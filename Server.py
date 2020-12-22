PORT = 8000
from http.server import BaseHTTPRequestHandler
import socketserver
import argparse
import json
from os import environ
# from datetime import datetime
import os
import numpy as np
import cv2
from decision import decision
from hconcat import save_hconcat
import stop_detection
import time

#region: argparser --white=default 150
parser=argparse.ArgumentParser()
parser.add_argument('--white', type=int, required=False, default=120)
args=parser.parse_args()
white=args.white
#endregion

httpd = None
DISPLAY = 'DISPLAY' in environ

image_num=0
stopped=0
# directory='./images/image_'+datetime.now().strftime('%y%b%d%H%M%S')
# pi_directory='./images/pi_image_'+datetime.now().strftime('%y%b%d%H%M%S')
directory='./images/image'
pi_directory='./images/pi_image'
h_directory='./images/h_image'
stop_directory='./images/stop_image'
white_directory='./images/white_image'
ostu_directory='./images/ostu_image'

def select_white(image, white):
    lower = np.uint8([white,white,white])
    upper = np.uint8([255,255,255])#pure white
    white_mask = cv2.inRange(image, lower, upper)#lower~upper preserve, others->0(black)
    return white_mask

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        global image_num
        global stopped
        self.send_response(200)
        self.send_header('X-Server2Client', '123')
        self.end_headers()

        # print('\n\n\nint..headers[Content-Length]={}'.format(int(self.headers['Content-Length'])))
        data = self.rfile.read(int(self.headers['Content-Length']))
        data = np.asarray(bytearray(data), dtype="uint8")
        received_mode=int(self.headers['mode'])
        # print('received_mode={}'.format(received_mode))
        stop_detection.mode=received_mode
        distance=int(self.headers['distance'])

        undistorted_img = cv2.imdecode(data, cv2.IMREAD_ANYCOLOR)
        gray = cv2.cvtColor(undistorted_img, cv2.COLOR_BGR2GRAY)
        ret3, ostu_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        white_image=select_white(undistorted_img,white)
        pi_image=ostu_image
        if distance<50:
            pi_image=white_image
        result,second=decision(pi_image,undistorted_img,gray)
        left = result[0]
        right = result[1]
        mode=stop_detection.mode
        motor_result = {"left": left, "right": right, "second": second, "mode": mode}
        self.wfile.write(bytes(json.dumps(motor_result), encoding='utf8'))

        # cv2.putText(undistorted_img,'distance={}'.format(distance),(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        cv2.putText(undistorted_img,'({0},{1})'.format(int(left),int(right)),(190,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        cv2.imshow('image', undistorted_img)
        cv2.imshow('pi_image',pi_image)
        cv2.imshow('gray',gray)
        #region: image save
        image_name='image_'+"{0:0=2d}".format(image_num)+'.png'
        image_num+=1
        path=os.path.join(directory, image_name)
        pi_path=os.path.join(pi_directory, image_name)
        stop_path=os.path.join(stop_directory, image_name)
        # white_path=os.path.join(white_directory, image_name)
        # ostu_path=os.path.join(ostu_directory, image_name)
        cv2.imwrite(path,undistorted_img)
        cv2.imwrite(pi_path,pi_image)
        cv2.imwrite(stop_path,gray)
        # cv2.imwrite(white_path,white_image)
        # cv2.imwrite(ostu_path,ostu_image)
        #endregion
        key=cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            save_hconcat()
            self.finish()
            # self.server.shutdown()
            self.server._BaseServer__shutdown_request = True

with socketserver.TCPServer(("0.0.0.0", PORT),
                            Handler,
                            bind_and_activate=False) as httpd:
    httpd.server = httpd
    httpd.allow_reuse_address = True
    httpd.server_bind()
    httpd.server_activate()
    print("HTTPServer Serving at port", PORT)
    httpd.serve_forever()
