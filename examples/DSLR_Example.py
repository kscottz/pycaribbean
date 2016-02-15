import logging
import os
import subprocess
import sys
import gphoto2 as gp
import time

def setup():
    """
    Attempt to attach to a gphoto device and grab the camera and context. Return the results.
    """
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    gp.check_result(gp.use_python_logging())
    context = gp.gp_context_new()
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera, context))
    text = gp.check_result(gp.gp_camera_get_summary(camera, context))
    print text.text
    return camera,context


def recurse_config(child,params={}):
    """
    The gphoto control structure is a byzantine swig structure.
    This function traverses it recursively and puts it in a
    nice python dictionary.
    """
    if(child.count_children() <= 0):
        my_choices = []
        try:
            n = child.count_choices()
            if( n > 0 ):
                for k in range(0,n):
                    my_choices.append(child.get_choice(int(k)))
        except:
            return my_choices
        return my_choices
    else:
        for i in range(0, child.count_children()):
            chill = child.get_child(i)
            name = chill.get_name()
            params[name] = recurse_config(chill,{})
        return params

def print_config_dict(cdict,lvl=""):
    """
    Print a the python config dictionary for a camera.
    """
    if isinstance(cdict,dict):
        for k,v in cdict.items():
            print "{0}{1}".format(lvl,k)
            print_config_dict(v,lvl+"\t")
    elif isinstance(cdict,list):
        for l in cdict:
            print "{0}{1}".format(lvl,l)
        return

def set_config(camera,context,config,path,value):
    """
    Given a gphoto camera, context, and config 
    traverse the path of the config tree and set
    a parameter value. The path is basically the nodes
    to address in the control structure. Once the config
    object has been modified we have to set it on the camera.
    """
    current = config
    for p in path:
        current = current.get_child_by_name(p)
    current.acquire()
    current.set_value(value)
    current.disown()
    gp.check_result(gp.gp_camera_set_config(camera,config, context))
    print "Set {0} to {1}".format(current.get_name(),current.get_value())


def capture_image(camera,context,name):
    """
    Use gphoto to capture an image and retrieve it.
    Place the file in /tmp/name
    """
    file_path = gp.check_result(gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE, context))
    target = os.path.join('/tmp', name)
    print 'Copying image to {0}'.format(target)
    camera_file = gp.check_result(gp.gp_camera_file_get(
            camera, file_path.folder, file_path.name,
            gp.GP_FILE_TYPE_NORMAL, context))
    gp.check_result(gp.gp_file_save(camera_file, target))
    gp.check_result(gp.gp_camera_exit(camera, context))

        
def main():
    # set up our camera.
    camera,context = setup()
    # grab a single test image. 
    capture_image(camera,context,"crap.jpg")
    # Get the configuration of the camera
    config = gp.check_result(gp.gp_camera_get_config(camera, context))
    # Pythonify and print the configuration of the camera so
    # we can see what parameters we can play with. 
    pconfig = recurse_config(config)
    print_config_dict(pconfig)
    # Put the camera in AV mode, or aperture priority. 
    # Camera needs this to fiddle with aperture. 
    set_config(camera,context,config,["capturesettings","autoexposuremode"],"AV")
    count = 0
    # for all of the available aperture settings...
    for param in pconfig["capturesettings"]["aperture"]:
        # get the camera configuration
        config = gp.check_result(gp.gp_camera_get_config(camera, context))
        # set the new configuration
        set_config(camera,context,config,["capturesettings","aperture"],param)
        # and capture an image.
        fname = "Capture{:0>5}.jpg".format(count)
        capture_image(camera,context,fname)
        count += 1

if __name__ == "__main__":
    sys.exit(main())

"""
Bonus points ... make the results into an animated gif
using image magick. 
mogrify -path ./ -resize 8x8% -quality 90 -format jpg *.jpg
convert -delay 1 -loop 0 *.jpg animated.gif
"""
