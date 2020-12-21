import numpy as np
import cv2

FGAIN=0.020
PGAIN=0.0353
pre_rl=0
DGAIN=0.01
# f=open("./data/pid.txt",'w')

def Pcontrol(pi_image,image,upper_limit):#black and white pi_image only
    height,width=pi_image.shape
    pi_image= pi_image[height-upper_limit:,:]
    height = upper_limit-1
    center=160
    left=0
    right=320

    cv2.line(image,(0,upper_limit),(319,upper_limit),(0,0,255),2)
    
    if pi_image[height][:center].min(axis=0)==255:
        left=0  
    else:
        left = pi_image[height][:center].argmin(axis=0)

    if pi_image[height][center:].max(axis=0)==0:
        right=width
    else: 
        right = center+pi_image[height][center:].argmax(axis=0)
    center = int((left+right)/2)

    # cv2.line(image,(left,0),(left,239),(0,0,255),1)
    # cv2.line(image,(right,0),(right,239),(0,0,255),1)
    # cv2.line(image,(center,0),(center,239),(0,0,255),1)

    pi_image= np.flipud(pi_image)
    mask = pi_image!= 0
    
    integral=np.where(mask.any(axis=0), mask.argmax(axis=0), height)
    left_sum = np.sum(integral[left:center])
    right_sum = np.sum(integral[center:right])
    forward_sum = np.sum(integral[center-50:center+50])
    #let's try uturn debugging
    total_sum=np.sum(integral[left:right])
    left_h=integral[left]
    right_h=integral[right-1]
    # cv2.putText(image,'l~r:sum={}'.format(total_sum),(5,200),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    # cv2.putText(image,'l_h={}'.format(left_h),(5,230),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)
    # cv2.putText(image,'r_h={}'.format(right_h),(200,230),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)
    # cv2.line(image,(center-50,0),(center-50,239),(0,0,255),1)
    # cv2.line(image,(center+50,0),(center+50,239),(0,0,255),1)
    # cv2.putText(image,'f({0}k)'.format(forward_sum//1000),(190,60),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    # cv2.putText(image,'l({0}k)'.format(left_sum//1000),(190,90),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    # cv2.putText(image,'r({0}k)'.format(right_sum//1000),(190,120),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

    speed=forward_sum*FGAIN
    # speed=65
    r_l=(right_sum-left_sum)
    control=PGAIN*r_l
    # cv2.putText(image,'speed:{0}'.format(int(speed)),(5,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    # cv2.putText(image,'control:{0}'.format(int(control)),(5,90),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    right_result=(speed-control)/2 #50+40=90
    left_result=(speed+control)/2  #50-40=10
    result=(left_result,right_result)
    second=0

    if total_sum< 12000 and abs(left_h-right_h)<15:#certain value
        cv2.putText(image,'U turn!',(100,100),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),2)
        result=(50,-50)
        second=2.5

    return result,second

def PDcontrol(pi_image,image,upper_limit):#black and white pi_image only
    global pre_rl
    height,width=pi_image.shape
    pi_image= pi_image[height-upper_limit:,:]
    height = upper_limit-1
    center=160
    left=0
    right=320

    cv2.line(image,(0,upper_limit),(319,upper_limit),(0,0,255),2)
    
    if pi_image[height][:center].min(axis=0)==255:
        left=0  
    else:
        left = pi_image[height][:center].argmin(axis=0)

    if pi_image[height][center:].max(axis=0)==0:
        right=width
    else: 
        right = center+pi_image[height][center:].argmax(axis=0)
    center = int((left+right)/2)

    cv2.line(image,(left,0),(left,239),(0,0,255),1)
    cv2.line(image,(right,0),(right,239),(0,0,255),1)
    cv2.line(image,(center,0),(center,239),(0,0,255),1)

    pi_image= np.flipud(pi_image)
    mask = pi_image!= 0
    
    integral=np.where(mask.any(axis=0), mask.argmax(axis=0), height)
    left_sum = np.sum(integral[left:center])
    right_sum = np.sum(integral[center:right])
    forward_sum = np.sum(integral[center-50:center+50])

    cv2.line(image,(center-50,0),(center-50,239),(0,0,255),1)
    cv2.line(image,(center+50,0),(center+50,239),(0,0,255),1)
    cv2.putText(image,'f({0}k)'.format(forward_sum//1000),(190,60),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.putText(image,'l({0}k)'.format(left_sum//1000),(190,90),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.putText(image,'r({0}k)'.format(right_sum//1000),(190,120),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

    speed=forward_sum*FGAIN
    # speed=65
    r_l=(right_sum-left_sum)
    if pre_rl==0:
        delta=0
    else:
        delta=pre_rl-r_l
    control=PGAIN*r_l+DGAIN*delta
    cv2.putText(image,'speed:{0}'.format(int(speed)),(5,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.putText(image,'control:{0}'.format(int(control)),(5,90),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    right_result=(speed-control)/2 #50+40=90
    left_result=(speed+control)/2  #50-40=10
    result=(left_result,right_result)
    # f.write("\n\npre_rl={}".format(pre_rl))
    # f.write("\nr_l={}".format(r_l))
    # f.write("\ndelta={}".format(delta))
    pre_rl=r_l
    return result