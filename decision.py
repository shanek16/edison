#from direction_choice import *
from area_choice import *
from marker_recognition import *
from stop_detection import stop_detection

def decision(pi_image,undistorted_img):

    result=area_choice(pi_image,undistorted_img,upper_limit=120)
    result,second=stop_detection(undistorted_img,result)
    result,second=marker_recognition(pi_image,undistorted_img,result,speed=50)#upadate result
    #pre_result=result
    return result,second