from ar_markers import detect_markers
import cv2
import numpy as np

with np.load('B.npz') as X:
    mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

parameters =  cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
second=0
Kpx=30
Kpt=40
front=40

def marker_sign(pi_image,image,result,speed):
    markers=detect_markers(pi_image)
    if len(markers)!=0:
        markerid=markers[0].id
        markers[0].highlite_marker(image)
        
        if markerid==114:
            print('marker detected 114')
            print('left!!')
            result=(-speed,speed) #left
            second=1
        
        elif markerid==922: 
            print('marker detected 922')
            print('right!!')
            result=(speed,-speed) #right
            second=.8

        elif markerid==2537: 
            print('marker detected 2537')
            print('stop!!')
            result=(0,0) #stop
            second=5

        else:
            result=result
            second=0
    else:
        result=result
        second=0
    return result,second
 
def marker_tvec(gray,image,result,second):
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    if np.all(ids != None):
        rvec, tvec ,_ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.1, mtx, dist)
        # print('\n\nrvec={}'.format(rvec))
        a=rvec[0][0][1]
        b=rvec[0][0][2]
        theta=a-b
        # print('a={}'.format(a))
        # print('b={}'.format(b))
        print('theta={}'.format(theta))
        cv2.putText(image,'theta={}'.format(theta),(5,230),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)
        x=-tvec[0][0][0]
        print('x={}'.format(x))
        cv2.putText(image,'x={}'.format(x),(5,200),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)
        left=front-Kpx*x-Kpt*theta
        right=front+Kpx*x+Kpt*theta
        result=(left,right)
        second=0
        for i in range(0, ids.size):
            cv2.aruco.drawAxis(image, mtx, dist, rvec[i], tvec[i], 0.1)
        cv2.aruco.drawDetectedMarkers(image, corners)
        # if ids[ids.size-1][0]==0:
        #     print('id:0 detected')
    else:
        result=result
        second=second
    return result,second

def marker_ostu(pi_image,image,gray,result,second):
    global image_num
    # global second
    ret3, th3 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    markers=detect_markers(th3)
    if len(markers)!=0:
        markerid=markers[0].id
        markers[0].highlite_marker(image)
        
        if markerid==114:
            print('marker detected 114')
            print('left!!')
            result=(-50,50) #left
            second=.8
        
        elif markerid==922: 
            print('marker detected 922')
            print('right!!')
            result=(50,-50) #right
            second=.8

        elif markerid==2537: 
            print('marker detected 2537')
            print('stop!!')
            result=(0,0) #stop
            second=5

        else:
            result=result
            second=second
    else:
        result=result
        second=second
    return result,second

#region cascade marker test
# import cv2
# marker_obj=cv2.CascadeClassifier('right.xml')
# def marker_detect_cascade(image,speed,result,cascade_classifier=marker_obj):#gray image(1=front 2=left 3=right)
#     cascade_obj = cascade_classifier.detectMultiScale(
#         image,
#         scaleFactor=1.5,
#         minNeighbors=5,
#         minSize=(16,16),           
#     )
#     if type(cascade_obj) !='numpy.ndarray':
#         return result,0
#     for (x_pos, y_pos, width, height) in cascade_obj:

#         if(width>=40):
#             print('CASCADE marker detected')
#             result=(speed,-speed)
#             return result,1
#         else:
#             result=result
#             print('none')
#             return result,0
#endregion
