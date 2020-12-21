import cv2
import numpy as np
import os

def save_hconcat():
    directory='./images/image'
    pi_directory='./images/pi_image'
    h_directory='./images/h_image'
    stop_directory='./images/stop_image'
    image_num=0

    for img in os.listdir(directory):
        image_name='image_'+"{0:0=2d}".format(image_num)+'.png'
        image_num+=1
        path=os.path.join(directory, image_name)
        pi_path=os.path.join(pi_directory, image_name)
        h_path=os.path.join(h_directory, image_name)
        stop_path=os.path.join(stop_directory, image_name)
        try:
            im1 = cv2.imread(path)
            im2 = cv2.imread(pi_path)
            im3 = cv2.imread(stop_path)
            im_h = cv2.hconcat([im1, im2, im3])
            cv2.imwrite(h_path, im_h)
        except:
            pass

# save_hconcat()