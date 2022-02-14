import numpy as np
import cv2
# import mrcnn.config
# import mrcnn.utils
# from mrcnn.model import MaskRCNN
from pathlib import Path
# import mrcnn.visualize
import map_pts
import pickle


# Конфигурация, которую будет использовать библиотека Mask-RCNN.
# class MaskRCNNConfig(mrcnn.config.Config):
#     NAME = "coco_pretrained_model_config"
#     IMAGES_PER_GPU = 1
#     GPU_COUNT = 1
#     NUM_CLASSES = 1 + 80  # в датасете COCO находится 80 классов + 1 фоновый класс.
#     DETECTION_MIN_CONFIDENCE = 0.6


def get_car_boxes(r):
    # Фильтруем список результатов распознавания, чтобы остались только автомобили.
    # Если найденный объект не автомобиль, то пропускаем его.
    return np.array([box for i, box in enumerate(r['rois']) if r['class_ids'][i] in [3, 8, 6]])


ROOT_DIR = Path(".")  # Корневая директория проекта.
# MODEL_DIR = ROOT_DIR / "logs"  # Директория для сохранения логов и обученной модели.
# COCO_MODEL_PATH = ROOT_DIR / "mask_rcnn_coco.h5"  # Локальный путь к файлу с обученными весами.
# if not COCO_MODEL_PATH.exists():  # Загружаем датасет COCO при необходимости.
#     mrcnn.utils.download_trained_weights(COCO_MODEL_PATH)
# model = MaskRCNN(mode="inference",
#                  model_dir=MODEL_DIR, config=MaskRCNNConfig())  # Создаём модель Mask-RCNN в режиме вывода.
# model.load_weights(COCO_MODEL_PATH.name, by_name=True)  # Загружаем предобученную модель.
# CLASS_NAMES = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
#                'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog',
#                'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag',
#                'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat',
#                'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork',
#                'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog',
#                'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv',
#                'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
#                'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
settings = {
    'frame_points': [[346, 633], [1500, 404], [2405, 474], [1228, 1403]],
    'map_points': [[705, 338], [1009, 697], [890, 1013], [398, 606]],
    'coord_points': [[55.857961, 37.350879], [55.857386, 37.351734], [55.856881, 37.351394], [55.857532, 37.349996]],
    'VIDEO_SOURCE': "frame_in_02.mp4",
    'MAP_SOURCE': "map.PNG"
}
interceptor = [699, 417]  # для ориентации кадра в большом кадре (в котором были измерены точки frame_points
settings['frame_points'] = (np.array(settings['frame_points']) - np.array(interceptor)).tolist()
mapping_point = map_pts.MappingPoints(settings)

_break = False
parked_car_boxes = None  # Местоположение парковочных мест.
video_capture = cv2.VideoCapture(
    mapping_point.VIDEO_SOURCE)  # Загружаем видеофайл, для которого хотим запустить распознавание.
image_map = cv2.imread(mapping_point.MAP_SOURCE)
free_space_frames = 0  # Сколько кадров подряд с пустым местом мы уже видели.
width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video_capture.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # MJPG
out = cv2.VideoWriter(mapping_point.VIDEO_SOURCE.split('.')[0] + '_output.avi', fourcc, fps, (width, height))
out_map = cv2.VideoWriter(mapping_point.MAP_SOURCE.split('.')[0] + '_output.avi', fourcc, fps, (1240, 1511))

try:
    while video_capture.isOpened():  # Проходимся в цикле по каждому кадру.
        success, frame, rgb_image = None, None, None
        _success, _frame, _rgb_image = [], [], []
        # for i in range(MaskRCNNConfig().BATCH_SIZE):
        #     success, frame = video_capture.read()
        #     rgb_image = frame[:, :, ::-1]  # Конвертируем изображение из цветовой модели BGR в RGB.
        #     _success += [success]
        #     _frame += [frame]
        #     _rgb_image += [rgb_image]
        #     if not success:
        #         break
        # if not success:
        #     break
        # results = model.detect(_rgb_image, verbose=1)  # Подаём изображение модели Mask R-CNN для получения результата.
        results = []

        for r, frame in zip(results, _frame):
            image = image_map.copy()
            # Mask R-CNN предполагает, что мы распознаём объекты на множественных изображениях.
            # Мы передали только одно изображение, поэтому извлекаем только первый результат.
            # r = results[0]
            # теперь используем каждый кадр

            # Переменная r теперь содержит результаты распознавания:
            # - r['rois'] — ограничивающая рамка для каждого распознанного объекта;
            # - r['class_ids'] — идентификатор (тип) объекта;
            # - r['scores'] — степень уверенности;
            # - r['masks'] — маски объектов (что даёт вам их контур).

            if parked_car_boxes is None:
                # Это первый кадр видео — допустим, что все обнаруженные машины стоят на парковке.
                # Сохраняем местоположение каждой машины как парковочное место и переходим к следующему кадру.
                parked_car_boxes = get_car_boxes(r)
                with open('saved_data.obj', 'wb') as f:
                    pickle.dump(r, f)
            else:
                # Мы уже знаем, где места. Проверяем, есть ли свободные.
                point_car = None
                # Ищем машины на текущем кадре.
                car_boxes = get_car_boxes(r)
                # Смотрим, как сильно эти машины пересекаются с известными парковочными местами.
                # overlaps = mrcnn.utils.compute_overlaps(parked_car_boxes, car_boxes)
                # Предполагаем, что свободных мест нет, пока не найдём хотя бы одно.
                free_space = False
                # Проходимся в цикле по каждому известному парковочному месту.
                # for parking_area, overlap_areas in zip(parked_car_boxes, overlaps):
                #
                #     # Ищем максимальное значение пересечения с любой обнаруженной
                #     # на кадре машиной (неважно, какой).
                #     max_IoU_overlap = np.max(overlap_areas)
                #
                #     # Получаем верхнюю левую и нижнюю правую координаты парковочного места.
                #     y1, x1, y2, x2 = parking_area
                #
                #     # Проверяем, свободно ли место, проверив значение IoU.
                #     if max_IoU_overlap < 0.15:
                #         # Место свободно! Рисуем зелёную рамку вокруг него.
                #         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                #         point_car = [(x1 + x2) / 2, y1 * 0.2 + y2 * 0.8]
                #         # Отмечаем, что мы нашли как минимум оно свободное место.
                #         free_space = True
                #     else:
                #         # Место всё ещё занято — рисуем красную рамку.
                #         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
                #
                #     # Записываем значение IoU внутри рамки.
                #     font = cv2.FONT_HERSHEY_DUPLEX
                #     cv2.putText(frame, f"{max_IoU_overlap:0.2}", (x1 + 6, y2 - 6), font, 0.3, (255, 255, 255))
                # Если хотя бы одно место было свободным, начинаем считать кадры.
                # Это для того, чтобы убедиться, что место действительно свободно
                # и не отправить лишний раз уведомление.
                if free_space:
                    free_space_frames += 1
                else:
                    # Если всё занято, обнуляем счётчик.
                    free_space_frames = 0
                # Если место свободно на протяжении нескольких кадров, можно сказать, что оно свободно.
                if free_space_frames > 10:
                    frame, image, coordinates = mapping_point.render_one_car(frame, image, point_car)
                    if free_space_frames == 11:
                        print(coordinates)

                    # Чтобы найти точку в Яндекс картах
                    # webbrowser.open(f'https://yandex.ru/maps/213/moscow/?ll={coordinates[1]}%2C{coordinates[0]}&mode=
                    # whatshere&whatshere%5Bpoint%5D={coordinates[1]}%2C{coordinates[0]}&whatshere%5Bzoom%5D=18&z=19',new=1)

                    # Отображаем надпись SPACE AVAILABLE!! вверху экрана. Теперь не отображаем
                    # font = cv2.FONT_HERSHEY_DUPLEX
                    # cv2.putText(frame, f"SPACE AVAILABLE!", (10, 150), font, 3.0, (0, 255, 0), 2, cv2.FILLED)
                else:
                    image = mapping_point.render_map(image)
                    frame = mapping_point.render_frame(frame)

                # Показываем кадр на экране.
                out.write(frame)
                cv2.imshow('Video', frame)
                out_map.write(image)
                cv2.imshow('Image', image)

            # Нажмите 'q', чтобы выйти.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                _break = True
                break
        if _break:
            break
except Exception as e:
    print(e)
finally:
    out.release()
    out_map.release()
    video_capture.release()
    cv2.destroyAllWindows()
    # os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
