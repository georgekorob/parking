# Установка

1. Создаем virtualenv python 3.9.5(тут скорей всего есть простор, главное не 3.10 - он не совместим)
2. В него устанавливаем yolov5 git clone https://github.com/ultralytics/yolov5.git
3. Устанавливаем все из yolov5/requirements.txt

pip install -r yolov5/requirements.txt

(в моем случае скачался неподдерживающий cuda pytorch и pytorchvision)
можно проверить разкомментирвав строку в test.py для проверки доступных девайсов.
Если там только CPU то нужно скачать для python 3.9(либо выбираем для нашей версии python):
windows:
torch: https://download.pytorch.org/whl/cu113/torch-1.10.0%2Bcu113-cp39-cp39-win_amd64.whl
trochvision: https://download.pytorch.org/whl/cu113/torchvision-0.11.1%2Bcu113-cp39-cp39-win_amd64.whl
linux:
torch: https://download.pytorch.org/whl/cu113/torch-1.10.0%2Bcu113-cp39-cp39-linux_x86_64.whl
trochvision: https://download.pytorch.org/whl/cu113/torchvision-0.11.1%2Bcu113-cp39-cp39-linux_x86_64.whl

и установить через :

pip install folder/file.whl

для установки все.

4. Скачать файл test.py и положить в корень yolov5
https://drive.google.com/drive/folders/1AdUtFcxWGAy8hHlHrJXtkufuk-yFGDsj?usp=sharing

5. Картинки и видео складываем в yolov5/data/images

6. запускаем test.py

7. Картинки и видео с рамками забираем в yolov5/runs/detect/exp
Текстовый файл с рамками и классами забираем в yolov5/runs/detect/exp/lables
боксы выдаются в формате на каждую картинку txt файл в нем каждая строка один бокс в формате: class x_center y_center width height.
8. там же где и test.py  лежит 3 предобученных модели.
s-512.pt самая маленькая
x-512.pt побольше
x-704.pt самая большая

 Любую из них кладем в корень yolov5, и прописываем в поле weights.
