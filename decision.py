from area_choice import Pcontrol
from marker_recognition import marker_recognition
from stop_detection import stop_detection

def decision(pi_image,undistorted_img):

    result=Pcontrol(pi_image,undistorted_img,upper_limit=120)
    result,second=stop_detection(undistorted_img,result)
    result,second=marker_recognition(pi_image,undistorted_img,result,speed=50)#upadate result
    #pre_result=result
    return result,second