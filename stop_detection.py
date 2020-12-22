import cv2

mode=0
# second=0

def stop_detection(gray,image,result,second):
    global mode
    # global second
    obj = cv2.CascadeClassifier('cascade.xml')
    cascade_obj = obj.detectMultiScale(
        gray,
        scaleFactor=1.02,
        minNeighbors=8,
        minSize=(40,40),
        maxSize=(80,80),
    )

    for (x_pos, y_pos, width, height) in cascade_obj:
        if(width>=40):
            cv2.rectangle(image, (x_pos, y_pos), (x_pos+width, y_pos+height), (255, 255, 255), 2)
            # cv2.putText(image, 'Stop', (x_pos, y_pos-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            # cv2.rectangle(gray, (x_pos, y_pos), (x_pos+width, y_pos+height), (255, 255, 255), 2)
            # cv2.putText(gray, 'Stop', (x_pos, y_pos-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            mode=mode+1#stop
    cv2.putText(image,'mode={}'.format(mode),(100,150),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    
    if mode>6:
        # print('in mode>5')
        # print('passing second to Client..')
        result=(0,0)
        second=3
    else:
        result=result
        second=second
    return result,second

def stop2(gray,image,result):
    global mode
    # obj = cv2.CascadeClassifier('stopsign.xml')
    obj = cv2.CascadeClassifier('cascade.xml')
    cascade_obj = obj.detectMultiScale(
        gray,
        scaleFactor=1.02,
        minNeighbors=6,
        minSize=(8,8),           
    )

    for (x_pos, y_pos, width, height) in cascade_obj:
        if(width>=40):
            cv2.rectangle(image, (x_pos, y_pos), (x_pos+width, y_pos+height), (255, 255, 255), 2)
            # cv2.putText(image, 'Stop', (x_pos, y_pos-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            # cv2.rectangle(gray, (x_pos, y_pos), (x_pos+width, y_pos+height), (255, 255, 255), 2)
            # cv2.putText(gray, 'Stop', (x_pos, y_pos-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            mode=mode+1#stop
    # cv2.putText(image,'mode={}'.format(mode),(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    
    if mode>=2 and mode<30:
        result=(0,0)
    else:
        result=result

    return result