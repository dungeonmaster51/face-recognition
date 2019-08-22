#!/usr/bin/env python

import joblib
import argparse
import cv2
import numpy as np
from PIL import Image


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        'Script for recognising faces on picture. Output of this script is json with list of people on picture and '
        'base64 encoded picture which has bounding boxes of people.')
    parser.add_argument('-m', '--model-path', required=True, help='Path to face recogniser model.')
    parser.add_argument('--image-path', required=True, help='Path to image file.')
    return parser.parse_args(args)


def draw_bb_on_img(faces, img):
    for face in faces:
        cv2.rectangle(img, (int(face.bb.left), int(face.bb.top)), (int(face.bb.right), int(face.bb.bottom)),
                      (0, 255, 0), 2)
        cv2.putText(img, "%s %.2f%%" % (face.top_prediction.name.upper(), face.top_prediction.confidence * 100),
                    (int(face.bb.left), int(face.bb.top) - 10), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 4,
                    cv2.LINE_AA)


def _recognise_faces(args):
    img = Image.open(args.image_path).convert('RGB')
    faces = joblib.load(args.model_path)(img)
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    draw_bb_on_img(faces, img_cv)
    return faces, img_cv


def main():
    args = parse_args()
    faces, img = _recognise_faces(args)
    cv2.imwrite('img.jpg', img)
    # cv2.imshow('image', img)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    # cv2.waitKey(1)


if __name__ == '__main__':
    main()
