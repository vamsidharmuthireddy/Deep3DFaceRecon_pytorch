
import cv2
import os
import json
import sys
import dlib
from imutils import face_utils


def detect_landmark_points(img_path, file_path):

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

    img = cv2.imread(img_path)
    #img = cv2.cvtColor(cv2.imread(path_to_image), cv2.COLOR_BGR2RGB)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale image
    rects = detector(gray, 1)

    if rects is not None:
        rect = rects[0]
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        f = open(file_path, 'w')

        for i, (x, y) in enumerate(shape):
            # print(x, y)
            f.write(f"{x} {y}")
            if i != shape.shape[0]-1:
                f.write("\n")

        f.close()


# img_path = sys.argv[1]
# file_path = os.path.splitext(img_path)[0] + ".txt"

# detect_landmark_points(img_path, file_path)
