from ar_markers import detect_markers
#import time

def marker_recognition(pi_image,image,result,speed):
    markers=detect_markers(pi_image)
    if len(markers)!=0:
        markerid=markers[0].id
        markers[0].highlite_marker(image)
        
        if markerid==114:
            print('marker detected 114')
            print('left!!')
            result=(-speed,speed) #left
            second=0
        
        elif markerid==922: 
            print('marker detected 922')
            print('right!!')
            result=(speed,-speed) #right
            second=0

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
 
# #############test#######################
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
    
