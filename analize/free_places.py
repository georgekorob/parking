import math
import numpy as np
import cv2
from pathlib import Path
import typing
import geometry as geom


class MappingPoints:
    def __init__(self, settings_map, car_boxes=None):
        import pickle, json
        if settings_map.get('interceptor'):
            settings_map['frame_points'] = (np.array(settings_map['frame_points']) -
                                            np.array(settings_map['interceptor'])).tolist()
        self.VIDEO_SOURCE = f"data/{settings_map.get('VIDEO_SOURCE')}"
        self.MAP_SOURCE = f"data/{settings_map.get('MAP_SOURCE')}"
        self.parking_lines = settings_map.get('parking_lines')
        self.frame_points = np.int32(settings_map['frame_points'])
        self.map_points = np.int32(settings_map['map_points'])
        self.coord_points = np.array(settings_map['coord_points'])
        self.transform_frame_to_map = cv2.getPerspectiveTransform(np.float32(self.frame_points),
                                                                  np.float32(self.map_points))
        self.transform_frame_to_coord = cv2.getPerspectiveTransform(np.float32(self.frame_points),
                                                                    np.float32(self.coord_points))
        self.transform_coord_to_map = cv2.getPerspectiveTransform(np.float32(self.coord_points),
                                                                  np.float32(self.map_points))
        self.transform_coord_to_frame = cv2.getPerspectiveTransform(np.float32(self.coord_points),
                                                                    np.float32(self.frame_points))
        # self.colors = [tuple(int(i) for i in np.random.choice(range(40, 256, 32), size=3)) for _ in
        #                range(len(self.parking_lines))]
        # self.colors = [(100, 100, 255), (255, 100, 255), (100, 255, 255), (255, 255, 100)]
        self.colors = [(100, 100, 255)] * len(self.parking_lines)
        # with open('data/saved_data.obj', 'rb') as f:
        #     self.parked_car_info = pickle.load(f)
        # self.car_boxes = self.get_car_boxes(self.parked_car_info)  # Достаем данные о найденных автомобилях
        # with open('data/car_boxes.obj', 'wb') as f:
        #     pickle.dump(self.car_boxes, f)
        if car_boxes:
            self.car_boxes = np.array(car_boxes)
        else:
            try:
                with open('data/car_boxes.obj', 'rb') as f:
                    self.car_boxes = pickle.load(f)
            except Exception as e:
                print(e)
        self.cam_point = None
        self.car_points = None
        self.m_in_degree = None
        self.parking_dict = None
        self.car_coords = None
        self.cam_height = np.int32(settings_map['cam_height'])
        self.angles = []

    def rectangle_car_boxes(self, frame):
        for parking_area in self.car_boxes:
            x1, y1, x2, y2 = parking_area
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
        return frame

    def render_points(self, frame_layer, data):
        if data['coord'] is not None and len(data['coord']) > 0:
            data_coord = [(int(p[0]), int(p[1])) for p in data['coord']]
            for p in data_coord:
                cv2.circle(frame_layer, p, radius=5, color=data['color'], thickness=data['thick'])

    def search_cam_xy(self):
        points = np.array([[0, 0], [0, 100], [100, 0], [100, 100]])
        points = geom.get_point_in_other(self.transform_frame_to_coord, points)
        self.cam_point = geom.intersection_array(points)
        self.m_in_degree = math.cos(self.cam_point[1]) * 111300
        self.cam_height = self.cam_height / self.m_in_degree

    @staticmethod
    def get_car_boxes(r):
        return np.array([box for i, box in enumerate(r['rois']) if r['class_ids'][i] in [3, 8, 6]])

    def get_car_points_from_boxes(self):
        cars = []
        for x1, y1, x2, y2 in self.car_boxes:
            pa = geom.get_point_in_other(self.transform_frame_to_coord, np.array([[(x1 + x2) / 2, y2]]))[0]
            alpha = geom.search_angle_between_points(pa, self.cam_point, self.cam_height)
            y = y2 - (y2 - y1) * math.tan(alpha)
            self.angles += [alpha]
            cars += [[(x1 + x2) / 2, y]]
        return np.array(cars)

    def parking_lines_coord(self):
        self.parking_lines = np.array([geom.get_point_in_other(self.transform_frame_to_coord, np.array(pl))
                                       for pl in self.parking_lines])

    def car_points_coord(self):
        self.car_coords = geom.get_point_in_other(self.transform_frame_to_coord, self.car_points)

    def perpendicular_dict(self):
        parking_lines_ab = geom.get_lines_from_array(self.parking_lines)
        parking_dict = []
        for i, (pl, pl_p) in enumerate(zip(parking_lines_ab, self.parking_lines)):
            park = {'park': i, 'cars': [], 'inter': [], 'lens': []}
            for j, car in enumerate(self.car_coords):
                point, leng = geom.get_perpendicular_to_line_from_point(pl, car)
                if leng < 1e-2 and pl_p[0][0] < point[0] < pl_p[1][0]:
                    park['cars'] += [j]
                    park['inter'] += [point]
                    park['lens'] += [leng]
            park['cars'], park['inter'], park['lens'] = np.array(park['cars']), \
                                                        np.array(park['inter']), \
                                                        np.array(park['lens'])
            parking_dict += [park]
        self.parking_dict = parking_dict

    def parking_sort_len(self):
        for pdict, pl in zip(self.parking_dict, self.parking_lines):
            # Определяем расстояния на парковке от начала парковки
            lens = np.array([geom.get_lenght(pl[0], p) for p in np.vstack((pdict['inter'], pl[1]))])
            ind_sort_lens = np.argsort(lens)  # Находим индексы сортировки расстояний
            lens = lens[ind_sort_lens]  # Сортируем расстояния
            lens = np.append(lens[0], lens[1:] - lens[:-1])  # Находим все расстояния между машинами и краями парка

            ind_sort_dict = ind_sort_lens[:-1]  # Формируем индексы сортировки автомобилей
            # Сортируем
            pdict['cars'], pdict['inter'], pdict['lens'] = pdict['cars'][ind_sort_dict], \
                                                           pdict['inter'][ind_sort_dict], \
                                                           pdict['lens'][ind_sort_dict]
            median = np.median(lens)  # [1:-1]
            median_lens = lens / median
            minimal = np.min(median_lens) * 1.1  # [1:-1]
            points_to_add = []

            for i, ml in enumerate(median_lens):
                result_point = pdict['inter'][np.min([i, len(pdict['inter']) - 1])]
                if i == len(pdict['inter']):
                    direction = 1
                    count = int(ml / minimal - 0.3)
                    len_to_calc = ml / (count + 0.5) * median
                else:
                    direction = -1
                    count = int(ml / minimal + 0.2) - 1
                    if count < 0:
                        continue
                    len_to_calc = ml / (count + 1) * median
                if count > 0:
                    for _ in range(count):
                        result_point = geom.get_point_on_line(result_point, pl, direction * len_to_calc)
                        points_to_add += [result_point]

            pdict['free'] = np.array(points_to_add)

    def render(self):
        # Получаем картинки
        image_map = cv2.imread(self.MAP_SOURCE)
        map_copy = image_map.copy()
        image_frame = cv2.imread(self.VIDEO_SOURCE)
        frame_copy = image_frame.copy()

        # Дополнительные данные
        self.search_cam_xy()  # Находим координаты камеры
        self.car_points = self.get_car_points_from_boxes()  # Определить точки машин
        self.car_points_coord()
        self.parking_lines_coord()  # Перевести координаты линий парковки в координаты
        # map_pl = [geom.get_point_in_other(self.transform_coord_to_map, pl) for pl in self.parking_lines]
        # map_cars = geom.get_point_in_other(self.transform_frame_to_map, self.car_points)
        # for line in map_pl:
        #     cv2.line(map_copy, tuple([int(l) for l in line[0]]), tuple([int(l) for l in line[1]]), (0, 0, 255), 2)
        # for pt in map_cars:
        #     cv2.circle(map_copy, tuple([int(p) for p in pt]), 4, (255, 0, 255), 1)
        # cv2.imshow('test', cv2.addWeighted(image_map, 0.5, map_copy, 0.5, 0.0))
        # cv2.waitKey(0)
        self.perpendicular_dict()  # Наити перпедникуляры
        self.parking_sort_len()  # Отсортировать автомобили

        frame_pl = [geom.get_point_in_other(self.transform_coord_to_frame, pl) for pl in self.parking_lines]
        frame_free = [geom.get_point_in_other(self.transform_coord_to_frame, pd['free']) for pd in self.parking_dict]
        map_cars = geom.get_point_in_other(self.transform_frame_to_map, self.car_points)
        map_pl = [geom.get_point_in_other(self.transform_coord_to_map, pl) for pl in self.parking_lines]
        map_free = [geom.get_point_in_other(self.transform_coord_to_map, pd['free']) for pd in self.parking_dict]
        color_free = (0, 255, 0)

        # Работа с кадром
        frame_copy = self.rectangle_car_boxes(frame_copy)  # Нарисовать боксы
        for park, line, color, ff in zip(self.parking_dict, frame_pl, self.colors, frame_free):
            # for park, line, color in zip(self.parking_dict, frame_pl, self.colors):
            self.render_points(frame_copy, {'coord': self.car_points[park['cars']], 'color': color, 'thick': 3})
            self.render_points(frame_copy, {'coord': ff, 'color': color_free, 'thick': 3})
            self.render_line_with_check(color, frame_copy, line)

        # Работа с картой
        for park, line, color, mf in zip(self.parking_dict, map_pl, self.colors, map_free):
            # for park, line, color in zip(self.parking_dict, map_pl, self.colors):
            self.render_points(map_copy, {'coord': map_cars[park['cars']], 'color': color, 'thick': 2})
            self.render_points(map_copy, {'coord': mf, 'color': color_free, 'thick': 2})
            self.render_line_with_check(color, map_copy, line)

        # Совмещение данных и визуализация
        image_frame, image_map = [cv2.addWeighted(c, 0.8, i, 0.2, 0.0) for c, i in
                                  [[frame_copy, image_frame], [map_copy, image_map]]]
        frame_with_map = self.standart_img(image_frame, image_map, 900)
        cv2.imshow('Detecting...', frame_with_map)
        # cv2.waitKey(0)
        while True:
            # Нажмите 'q', чтобы выйти.
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('q'), ord('й')]:
                break
        cv2.destroyAllWindows()

    def render_for_an(self, image_frame):
        # Получаем картинки
        frame_copy = image_frame.copy()

        # Дополнительные данные
        self.search_cam_xy()  # Находим координаты камеры
        self.car_points = self.get_car_points_from_boxes()  # Определить точки машин
        self.car_points_coord()
        self.parking_lines_coord()  # Перевести координаты линий парковки в координаты
        self.perpendicular_dict()  # Наити перпедникуляры
        self.parking_sort_len()  # Отсортировать автомобили

        frame_pl = [geom.get_point_in_other(self.transform_coord_to_frame, pl) for pl in self.parking_lines]
        park_free_c = [pd['free'] for pd in self.parking_dict if pd]
        frame_free = [geom.get_point_in_other(self.transform_coord_to_frame, p) for p in park_free_c]
        color_free = (0, 255, 0)

        # Работа с кадром
        frame_copy = self.rectangle_car_boxes(frame_copy)  # Нарисовать боксы
        for park, line, color, ff in zip(self.parking_dict, frame_pl, self.colors, frame_free):
            # for park, line, color in zip(self.parking_dict, frame_pl, self.colors):
            self.render_points(frame_copy, {'coord': self.car_points[park['cars']], 'color': color, 'thick': 3})
            self.render_points(frame_copy, {'coord': ff, 'color': color_free, 'thick': 3})
            self.render_line_with_check(color, frame_copy, line)

        # Совмещение данных и визуализация
        image_frame_to_return = cv2.addWeighted(frame_copy, 0.8, image_frame, 0.2, 0.0)
        return image_frame_to_return, frame_free, park_free_c

    def standart_img(self, image_frame, image_map, width=200):
        (mh, mw, _), (fh, fw, _) = image_map.shape, image_frame.shape
        image_map = cv2.resize(image_map, (width, int(mh/mw*width)))
        image_frame = cv2.resize(image_frame, (width, int(fh/fw*width)))
        frame_with_map = np.concatenate((image_frame, image_map), axis=0)
        return frame_with_map

    def render_line_with_check(self, color, frame_copy, line):
        line = np.int32(line)
        cv2.line(frame_copy, line[0], line[1], color=color, thickness=2)


if __name__ == '__main__':
    import json

    file_name = 'data/setting.json'
    with open(file_name, 'r') as f:
        settings = json.load(f)
    MappingPoints(settings).render()
