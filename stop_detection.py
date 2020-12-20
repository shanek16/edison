import cv2
import os

stop_directory='./images/stop_negative'
image_num=0

mode=0
def stop_detection(image,result):
    global mode
    global image_num
    obj = cv2.CascadeClassifier('stopsign.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade_obj = obj.detectMultiScale(
        gray,
        scaleFactor=1.02,
        minNeighbors=8,
        minSize=(10,10),           
    )

    for (x_pos, y_pos, width, height) in cascade_obj:
        if(width>=40):
            cv2.rectangle(image, (x_pos, y_pos), (x_pos+width, y_pos+height), (255, 255, 255), 2)
            # cv2.putText(image, 'Stop', (x_pos, y_pos-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            # cv2.rectangle(gray, (x_pos, y_pos), (x_pos+width, y_pos+height), (255, 255, 255), 2)
            # cv2.putText(gray, 'Stop', (x_pos, y_pos-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            mode=mode+1#stop
            print('mode: ',mode)
    if mode>2:
        print('in mode>3')
        print('passing second to Client..')
        result=(0,0)
        second=3
        mode=0
    else:
        result=result
        second=0
    cv2.imshow('stop_image',gray)
    '''image_name='image_'+"{0:0=2d}".format(image_num)+'.png'
    image_num+=1
    stop_path=os.path.join(stop_directory, image_name)
    cv2.imwrite(stop_path,gray)'''
    return result,second