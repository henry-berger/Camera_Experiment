import random
import numpy as np
import sys
from PIL import Image # image display

sys.path.append('../')
import utils

try:
    from pyspin import PySpin # Camera control
except:
    try:
        import PySpin
    except:
        print("FAILURE: COULDN'T IMPORT CAMERA LIBRARY (PySpin)")

class CCD():
#************************ Setup **************************#
    def __init__(self,parent=None,port=None):
        self.t0 = utils.gt() # just in case, but this should be reset when the data collection actually starts        
        if parent is not None:
            parent.CCD_start_time=self.t0
        else:
            print("Fail")
    def time(self):
        return utils.gt()-self.t0
    
    def get_file_name(self):
        return 'Most Recent Photo.jpg'
    
    def clear_cam(self):
        pass
        
    def take_picture(self):
#             try:
#                 del image_primary
#             except: pass

        # Get system
            system = PySpin.System.GetInstance()
    
        # Get camera list
            cam_list = system.GetCameras()
            if len(cam_list)==0:
                fccd = Fake_CCD(t=self.t0)
                return fccd.take_picture()
    
        # Figure out which is primary and secondary (usually webcam is primary and Flea3 is secondary)
            cam = cam_list.GetByIndex(0) 
            
            try: # in case the camera is already streaming
                cam.EndAcquisition()
            except: pass
            try: # in case the camera is already streaming
                cam.DeInit()
            except: pass
            
        # Initialize camera
            cam.Init()

        # Set acquisition mode
            cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_SingleFrame)

        # Start acquisition
            cam.BeginAcquisition()

        # Acquire images
            self.t1 = self.time()
            image_primary = cam.GetNextImage()
            self.t2 = self.time()
            width = image_primary.GetWidth()
            height = image_primary.GetHeight()
#             print ("width: " + str(width) + ", height: " + str(height))

        # Pixel array (NumPy array)
            raw_image_array = image_primary.GetData()
#             image_array=raw_image_array.reshape(height, width)

        # Save images
#             def image_save_function(ip):
            if True:
                image_primary.Save(self.get_file_name())
#             thread_do(f=image_save_function, args=(ip),wait=True)

        # Stop acquisition
            cam.EndAcquisition()

        # De-initialize
            cam.DeInit()

#         # Clear references to images and cameras
        # Clear references to images and cameras
            del image_primary
            del cam
            del cam_list

#             try:
#                 del image_primary
#             except:
#                 print("Couldn't delete image_primary")
#             try:
#                 del cam
#             except:
#                 print("Couldn't delete cam")
#             try:
#                 del cam_list
#             except:
#                 print("Couldn't delete cam_list")

        # return
            return raw_image_array, [height, width], [self.t1, self.t2]


class Fake_CCD():
#************************ Setup **************************#
    def __init__(self, t, port_name="None"):
        self.t0 = t
#         self.t0 = gt() # just in case, but this should be reset when the data collection actually starts

#********************** Reading **************************#        
    def time(self):
        return 12345.678 #gt()-self.t0        
        
    def pixelAssign(self,x,y): #############################################################################################
    #     dist = 100
    #     for xc in [-0.5,0,0.5]:
    #         for yc in [-0.5,0,0.5]:
    #             d = np.sqrt((x-xc)**2+(y-yc)**2)
    # #             print(dist)
    #             if d<dist:
    #                 dist = d
    #                 v = dist*np.absolute(xc + yc)
#         pass
        return random.random()*255
#         return (np.abs(x//0.25*0.25)+np.abs(y//0.25*0.25)+random.random())*80

    def imArray(self,xs, ys): #############################################################################################
        xlen, ylen = len(xs), len(ys);
        array = np.zeros([xlen, ylen]);
        for i in range(0, xlen):
            for j in range(0, ylen):
                x,y = xs[i],ys[j];
                array[-j,i] = self.pixelAssign(x,y)            
        return array

    def take_picture(self): #############################################################################################
#         self.t1 = self.time()
        w = 1
        res = 10
        xs = np.linspace(-w,w, res)
        ys = np.linspace(-w,w, res)
        array = self.imArray(xs,ys)
        array = np.array(array, dtype=np.uint8)
        im = Image.fromarray(array)
        im.save("Most Recent Photo.jpg")
        self.t1 = self.time()
        self.t2 = self.time()
        return np.concatenate(array), [res, res], [self.t1, self.t2]