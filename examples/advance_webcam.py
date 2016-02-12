import numpy as np
import cv2
import time

# create a map to keep track of all these names
prop_map = {
    "pos_msec":cv2.cv.CV_CAP_PROP_POS_MSEC,
    "pos_frame":cv2.cv.CV_CAP_PROP_POS_FRAMES,
    "avi_ratio":cv2.cv.CV_CAP_PROP_POS_AVI_RATIO ,
    "width":cv2.cv.CV_CAP_PROP_FRAME_WIDTH ,
    "height":cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ,
    "fps":cv2.cv.CV_CAP_PROP_FPS ,
    "fourcc":cv2.cv.CV_CAP_PROP_FOURCC ,
    "frame_count":cv2.cv.CV_CAP_PROP_FRAME_COUNT,
    "format":cv2.cv.CV_CAP_PROP_FORMAT ,
    "mode":cv2.cv.CV_CAP_PROP_MODE ,
    "brightness":cv2.cv.CV_CAP_PROP_BRIGHTNESS ,
    "contrast":cv2.cv.CV_CAP_PROP_CONTRAST ,
    "saturation":cv2.cv.CV_CAP_PROP_SATURATION,
    "hue":cv2.cv.CV_CAP_PROP_HUE ,
    "gain":cv2.cv.CV_CAP_PROP_GAIN ,
    "exposure":cv2.cv.CV_CAP_PROP_EXPOSURE ,
    "convert_rgb":cv2.cv.CV_CAP_PROP_CONVERT_RGB ,
 #   "white_balance":cv2.cv.CV_CAP_PROP_WHITE_BALANCE ,
    "rectification":cv2.cv.CV_CAP_PROP_RECTIFICATION}

# get a camera property
def get_prop(cam,name,prop_map):
    return cam.get(prop_map[name])

# set a camera property
def set_prop(cam,name,prop_map,value):
    cam.set(prop_map[name],value)

# print out all of the properites
def poll_props(cam,prop_map):
    out_map = {}
    for k,v in prop_map.items():
        result = cam.get(v)
        if( result == -1.0 ):
            out_map[k] = None
        else:
            out_map[k] = result
    return out_map

# create a camera and get its property
cam = cv2.VideoCapture(0)
properties = poll_props(cam,prop_map)

# list our properties
for k,v in properties.items():
    print "{0:<12}\t:{1:<12}".format(k,v)

while(True):
    # toggle properties and get results. 
    sat = get_prop(cam,"saturation",prop_map)
    if( sat > 0.5 ):
        set_prop(cam,"saturation",prop_map,o0.1)
    else:
        set_prop(cam,"saturation",prop_map,1.0)
    time.sleep(0.05)
    ret, frame = cam.read()
    cv2.imshow('Basic Web Cam',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# put our toys back on the shelf 
cam.release()
cv2.destroyAllWindows()
