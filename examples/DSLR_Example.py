import logging
import os
import subprocess
import sys
import gphoto2 as gp
import time

def setup():
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
    if isinstance(cdict,dict):
        for k,v in cdict.items():
            print "{0}{1}".format(lvl,k)
            print_config_dict(v,lvl+"\t")
    elif isinstance(cdict,list):
        for l in cdict:
            print "{0}{1}".format(lvl,l)
        return

def set_config(camera,context,config,path,value):
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
    camera,context = setup()
    capture_image(camera,context,"crap.jpg")
    config = gp.check_result(gp.gp_camera_get_config(camera, context))
    pconfig = recurse_config(config)
    print_config_dict(pconfig)
    count = 0
    set_config(camera,context,config,["capturesettings","autoexposuremode"],"AV")
    for param in pconfig["capturesettings"]["aperture"]:
        config = gp.check_result(gp.gp_camera_get_config(camera, context))
        set_config(camera,context,config,["capturesettings","aperture"],param)
        print param
        fname = "Capture{0}.jpg".format(count)
        capture_image(camera,context,fname)
        count += 1

if __name__ == "__main__":
    sys.exit(main())
