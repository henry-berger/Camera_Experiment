from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Image_Widget(QLabel):
# A pixmap image that scales to the largest it can be

    def __init__(self, parent=None, pixmap = None):
        super().__init__(parent)
        self.window = parent.window
        self.setScaledContents(False)
        
    # add a pixmap        
    def setMyPixmap(self, pixmap): #############################################################################################
        self.mypixmap = QPixmap(pixmap)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        # store the original, so scaling down and up doesn't cause pixelation
        self.originalpixmap = self.mypixmap
        self.setPixmap(self.mypixmap)
        
        # width and height
        self.W = self.mypixmap.width()
        self.H = self.mypixmap.height()
        try:
            self.WH = self.W / self.H
        except: self.WH = 1

        # resizing
        self.window.resized.connect(self.myresize)
        self.setMinimumSize(100, 300)
        self.setStyleSheet("height: auto; width: auto;")

    def myresize(self):  #############################################################################################
        # get the current dimensions
        w  = self.frameGeometry().width()
        h  = self.frameGeometry().height()
        # The image will naturally stretch to fill the whole widget
        # therefore, decrease w or h to match whichever is more constrained
        if w/h > self.WH:
            w = int(h * self.WH)
        elif w/h < self.WH:
            h = int(w/self.WH)
        # scale and implement
        self.mypixmap = self.originalpixmap.scaled(w,h)
        self.setPixmap(self.mypixmap)