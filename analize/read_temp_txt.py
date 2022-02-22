import pickle
import numpy as np
import cv2

frame = cv2.imread('../aineuro/exp/temp.jpg')
# frame2 = frame.copy()

DIM = (1920, 1080)
K = np.array([[1.26125746e+03, 0.00000000e+00, 9.40592038e+02],
              [0.00000000e+00, 1.21705719e+03, 5.96848905e+02],
              [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
D = np.array([-0.49181345, 0.25848255, -0.01067125, -0.00127517])
# newcameramtx, roi = cv2.getOptimalNewCameraMatrix(K, D, DIM, 1, DIM)
# undistorted_img = cv2.undistort(frame, K, D, None, newcameramtx)
Knew = K.copy()
Knew[(0, 1), (0, 1)] = 0.5 * Knew[(0, 1), (0, 1)]
map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), Knew, DIM, cv2.CV_16SC2)
undistorted_img = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

cv2.imshow('img', undistorted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# xl = 1920
# yl = 1080
#
# with open('../aineuro/exp/labels/temp.txt', 'r') as f:
#     for line in f.readlines():
#         box = [float(p) for p in line.split(' ')[1:]]
#         box = [(box[0]-box[2]/2)*xl, (box[1]-box[3]/2)*yl, (box[0]+box[2]/2)*xl, (box[1]+box[3]/2)*yl]
#         b0, b1, b2, b3 = [int(b) for b in box]
#         cv2.rectangle(frame2, (b0, b1), (b2, b3), (255, 0, 255), thickness=1)
#
# dst = cv2.addWeighted(frame, 0.2, frame2, 0.8, 0.0)
# cv2.imshow('img', dst)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# with open('../../../Home_Parking/data/car_boxes.obj', 'rb') as f:
#     car_boxes = pickle.load(f)

# print(car_boxes)
