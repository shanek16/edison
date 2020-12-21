from area_choice import Pcontrol
from marker_recognition import marker_ostu
# from marker_recognition import marker_tvec
from stop_detection import stop_detection
# from stop_detection import stop2

def decision(pi_image,undistorted_img,gray):

    result,second=Pcontrol(pi_image,undistorted_img,upper_limit=120)
    result,second=stop_detection(gray,undistorted_img,result)
    # result=stop2(gray,undistorted_img,result)
    result,second=marker_ostu(pi_image,undistorted_img,gray,result)
    # result,second=marker_tvec(pi_image,undistorted_img,result,speed=50)
    #pre_result=result
    return result,second