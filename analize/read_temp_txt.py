import cv2

frame = cv2.imread('../aineuro/exp/temp.jpg')
frame2 = frame.copy()
xl = 1920
yl = 1080

with open('../aineuro/exp/labels/temp.txt', 'r') as f:
    for line in f.readlines():
        box = [float(p) for p in line.split(' ')[1:]]
        box = [(box[0]-box[2]/2)*xl, (box[1]-box[3]/2)*yl, (box[0]+box[2]/2)*xl, (box[1]+box[3]/2)*yl]
        b0, b1, b2, b3 = [int(b) for b in box]
        cv2.rectangle(frame2, (b0, b1), (b2, b3), (255, 0, 255), thickness=1)

dst = cv2.addWeighted(frame, 0.2, frame2, 0.8, 0.0)
cv2.imshow('img', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
