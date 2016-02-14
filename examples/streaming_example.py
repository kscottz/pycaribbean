"""
Read and display a simple MJPEG stream given a URL
""" 
import cv2
import urllib 
import numpy as np
# open our url stream
stream=urllib.urlopen('http://192.168.1.228:8080/video')
# create a buffer of bytes
bytes=''
invert = False
while True:
    # read some bytes from the stream
    # how much to read is a matter of taste
    bytes+=stream.read(1024*8)
    # \xff\xd8 is the start of a jpg
    # \xff\xd9 is the end of a jpg
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    # if we find them
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2] # create a buffer
        bytes= bytes[b+2:] # save the remaining bytes
        #numpy can handle strings as image data
        img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
        # Add some bling to show we can process
        if invert:
            img = 255-img
        # show our image
        cv2.imshow("live_and_direct",img)
    # MVP keyboard input
    my_key = cv2.waitKey(1)
    if my_key & 0xFF == ord('q'):
        break
    if my_key & 0xFF == ord('i'):
        invert = not invert 
# put our toys away when done. 
stream.close()
cv2.destroyAllWindows()
