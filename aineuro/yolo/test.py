import utils
display = utils.notebook_init() #uncomment for GPU check 
import detect

detect.run(
    weights='s-512.pt',
    imgsz=(1920, 1080),
    conf_thres=0.25,
    source='data/images/test.jpg',
    classes=(0,),
    save_txt=True #save txt file with boxes to /runs/detect/exp/labels
)

