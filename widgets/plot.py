from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Plot_Widget(QWidget):
    def __init__(self,parent):
        super(Plot_Widget, self).__init__(parent)
#         print("Done")
        self.p = parent # the pump interface, with all the functions
        self.init_plot_UI()
        
    def init_plot_UI(self):
        self.plot_widget = QWidget()
        self.plot_layout = QGridLayout(self.plot_widget)
        self.plot_layout.setRowStretch(2,0)

        self.TEXT_HEIGHT = 28
        self.row = 0
        
#**************** Status Bar ******************#
        """    # setup
        self.progress_widget = QWidget()
        self.progress_layout = QHBoxLayout(self.progress_widget)
        self.plot_layout.addWidget(self.progress_widget,self.row,0,1,0)
    # label 0%
        lab0 = QLabel("0%")
        self.progress_layout.addWidget(lab0,alignment=Qt.AlignRight)
    # slider
        self.progress = QSlider(Qt.Horizontal,parent=self)
#         self.progress = QProgressBar(parent=self)
        self.progress_layout.addWidget(self.progress)
    # setup
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setEnabled(False)
        self.progress.setFixedHeight(30)
        self.progress.setMaximumWidth(640)
    # label 100%
        lab100 = QLabel("100%")
        self.progress_layout.addWidget(lab100,alignment=Qt.AlignLeft)
        self.progress_widget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        """
        self.row += 1

#         self.blank = QLabel("")
#         self.blank.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
#         self.plot_layout.addWidget(self.blank,self.row,0)       
        
#         self.row += 1
