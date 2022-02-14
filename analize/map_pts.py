import numpy as np
import cv2


class MappingPoints:
    """Класс для конвертирования точек из одной системы координат в другую и отображения."""
    def __init__(self, settings_map):
        self.frame_points = np.int32(settings_map['frame_points'])
        self.map_points = np.int32(settings_map['map_points'])
        self.coord_points = np.array(settings_map['coord_points'])
        self.VIDEO_SOURCE = settings_map['VIDEO_SOURCE']
        self.MAP_SOURCE = settings_map['MAP_SOURCE']
        self.transform_frame_to_map = cv2.getPerspectiveTransform(np.float32(self.frame_points),
                                                                  np.float32(self.map_points))
        self.transform_frame_to_coord = cv2.getPerspectiveTransform(np.float32(self.frame_points),
                                                                    np.float32(self.coord_points))

    @staticmethod
    def render_image_with_points(frame, points, point=None):
        """
        Рендер точек и сетки на изображении.
        :param frame: Изображение
        :param points: Сетка и её точки
        :param point: Точка парковки
        :return: Изображение
        """
        frame_layer = frame.copy()
        for p in points:
            cv2.circle(frame_layer, tuple(p.tolist()), radius=5, color=(255, 200, 200), thickness=3)
        if not point is None:
            cv2.circle(frame_layer, tuple(point[0].tolist()[:2]), radius=5, color=(100, 255, 100), thickness=3)
        cv2.polylines(frame_layer, [points.reshape((-1, 1, 2))], 4, color=(255, 200, 200), thickness=3)
        frame = cv2.addWeighted(frame_layer, 0.8, frame, 0.2, 0.0)
        return frame

    @staticmethod
    def get_real_points(lambda_tr, points):
        if isinstance(points, list):
            points = np.array(points)
        if points.ndim == 1:
            points = points.reshape(-1, 2)
        real_points = np.dot(lambda_tr, np.c_[points, np.ones(points.shape[0])].T).T
        return np.divide(real_points.T, real_points[:, 2]).T

    def render_frame(self, frame=None, frame_point_car=None):
        """
        Рендер точек и сетки на кадре.
        :param frame: Кадр
        :param frame_point_car: Точки
        :return: Кадр
        """
        if frame is None:
            frame = cv2.VideoCapture(self.VIDEO_SOURCE)
            success, frame = frame.read()
        return self.render_image_with_points(frame, self.frame_points, frame_point_car)

    def render_map(self, frame=None, map_point_car=None):
        """
        Рендер точек и сетки на карте.
        :param frame: Карта
        :param map_point_car: Точки
        :return: Карта
        """
        if frame is None:
            frame = cv2.imread(self.MAP_SOURCE)
        return self.render_image_with_points(frame, self.map_points, map_point_car)

    def render_one_car(self, frame_image, map_image, frame_point_car):
        """
        Отображение точки frame_point_car на кадре и карте.
        :param frame_image: Кадр
        :param map_image: Карта
        :param frame_point_car: Точка на кадре
        :return: Кадр, Карта, Мировые координаты точки
        """
        frame_point_car = np.int32([frame_point_car])
        map_point_car = np.int32(self.get_real_points(self.transform_frame_to_map, frame_point_car))
        coord_point_car = self.get_real_points(self.transform_frame_to_coord, frame_point_car)[0]
        frame_image = self.render_frame(frame=frame_image, frame_point_car=frame_point_car)
        map_image = self.render_map(frame=map_image, map_point_car=map_point_car)
        return frame_image, map_image, coord_point_car

    def render_one_frame(self, frame_point_car=None):
        import webbrowser
        if not frame_point_car is None:
            frame_point_car = np.int32([frame_point_car])
            map_point_car = np.int32(self.get_real_points(self.transform_frame_to_map, frame_point_car))
            coord_point_car = self.get_real_points(self.transform_frame_to_coord, frame_point_car)[0]
            #webbrowser.open(
            #    f'https://yandex.ru/maps/213/moscow/?ll={coord_point_car[1]}%2C{coord_point_car[0]}&mode=whatshere&whatshere%5Bpoint%5D={coord_point_car[1]}%2C{coord_point_car[0]}&whatshere%5Bzoom%5D=18&z=19',
            #    new=1)
        else:
            map_point_car = None
        frame_img = self.render_frame(frame=None, frame_point_car=frame_point_car)
        cv2.imshow('Video', frame_img)
        map_img = self.render_map(frame=None, map_point_car=map_point_car)
        cv2.imshow('Image', map_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    settings = {
        'frame_points': [[346, 633], [1500, 404], [2405, 474], [1228, 1403]],
        'map_points': [[705, 338], [1009, 697], [890, 1013], [398, 606]],
        'coord_points': [[55.857961, 37.350879], [55.857386, 37.351734], [55.856881, 37.351394],
                         [55.857532, 37.349996]],
        'VIDEO_SOURCE': "frame_in_02.mp4",
        'MAP_SOURCE': "map.PNG"
    }
    point_car = [346, 633]
    #interceptor = [699, 417]
    #settings['frame_points'] = (np.array(settings['frame_points']) - np.array(interceptor)).tolist()
    #point_car = (np.array(point_car) - np.array(interceptor)).tolist()
    mapping_point = MappingPoints(settings)
    mapping_point.render_one_frame(point_car)
    # координаты, карта, пиксели, видео
    # [55.857961, 37.350879], лево(перекресток тратуаров), [346, 633], верх, [705, 338]
    # [55.857386, 37.351734], верх(пешеходный переход), [1500, 404], право, [1009, 697]
    # [55.856881, 37.351394], право(внутренний угол дома), [2405, 474], низ, [890, 1013]
    # [55.857532, 37.349996], лево, [1228, 1403], низ(угол пристройки), [398, 606]
