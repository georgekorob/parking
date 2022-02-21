import numpy as np
import math


def get_point_in_other(lambda_tr, points):
    if len(points) > 0:
        real_points = np.dot(lambda_tr, np.c_[points, np.ones(points.shape[0])].T).T
        return np.divide(real_points.T, real_points[:, 2]).T[:, :2]


def intersection_array(points):
    return intersection_segments(points[:2], points[2:])


def intersection_segments(A, B):
    return intersection_points(A[0], A[1], B[0], B[1])


def intersection_points(a1, a2, b1, b2):
    ax1, ay1, ax2, ay2, bx1, by1, bx2, by2 = a1[0], a1[1], a2[0], a2[1], b1[0], b1[1], b2[0], b2[1]
    A1, B1, C1 = ay1 - ay2, ax2 - ax1, ax1 * ay2 - ax2 * ay1
    A2, B2, C2 = by1 - by2, bx2 - bx1, bx1 * by2 - bx2 * by1
    cam_y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
    cam_x = 0
    if B1 * A2 - B2 * A1 and A1:
        cam_x = (-C1 - B1 * cam_y) / A1
    elif B1 * A2 - B2 * A1 and A2:
        cam_x = (-C2 - B2 * cam_y) / A2
    return cam_x, cam_y


def search_angle_between_points(p1, p2, height):
    return math.atan(height / get_lenght(p1, p2))


def get_line_ab_from_line(line):
    return get_line_from_2_points(line[0], line[1])


def get_line_from_2_points(p1, p2):
    x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]
    a = (y1 - y2) / (x1 - x2)
    return a, y1 - x1 * a


def get_lines_from_array(points):
    lines = []
    for p1, p2 in points:
        lines += [get_line_from_2_points(p1, p2)]
    return lines


def get_perpendicular_to_line_from_point(line, point):
    xp = (line[0] * (point[1] - line[1]) + point[0]) / (line[0] ** 2 + 1)
    yp = xp * line[0] + line[1]
    return [xp, yp], ((point[0] - xp) ** 2 + (point[1] - yp) ** 2) ** 0.5


def get_lenght(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def get_point_on_line(p1, line, interval):
    a, _ = get_line_ab_from_line(line)
    alpha = math.atan(a)
    dx = math.cos(alpha) * interval
    dy = math.sin(alpha) * interval
    return [p1[0] + dx, p1[1] + dy]
