from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Output_Widget(QWidget):
    def __init__(self,parent):
        super(Output_Widget, self).__init__(parent)
#         print("Done")
        self.p = parent # the pump interface, with all the functions
        self.init_output_UI()
        
    def init_output_UI(self):
        self.output_widget = QWidget()
        self.layout = QGridLayout(self.output_widget)
        self.output_layout = QGridLayout()
        self.output_layout.setRowStretch(2,0)

        self.TEXT_HEIGHT = 28
        self.row = 0
        
        self.olabel = QLabel("Output")
        self.output_layout.addWidget(self.olabel,self.row,0,1,0,alignment=Qt.AlignHCenter)
        self.olabel.setFont(QFont('Arial', 10))
        self.olabel.setFixedHeight(32)
    
    
# These labels will be changed as the variables change
        self.readings_layout = QGridLayout()
    
#************************ Time **************************#
        self.row += 1
    # label
        self.time_label = QLabel("Time:")
        self.readings_layout.addWidget(self.time_label,self.row,0,alignment=Qt.AlignRight)
    # reading
        self.time_display = QLabel("--")
        self.readings_layout.addWidget(self.time_display,self.row,1,alignment=Qt.AlignLeft)
        self.time_display.setFixedHeight(self.TEXT_HEIGHT)

#******************* Stage Position ********************#
        self.row += 1
    # label
        self.liquid_label = QLabel("Current Liquid:")
        self.readings_layout.addWidget(self.liquid_label,self.row,0,alignment=Qt.AlignRight)
    # reading
        self.liquid_display = QLabel("--")
        self.readings_layout.addWidget(self.liquid_display,self.row,1,alignment=Qt.AlignLeft)
        self.liquid_display.setFixedHeight(self.TEXT_HEIGHT)
        
        self.output_layout.addLayout(self.readings_layout,self.row,0,1,0)
        

#**************** Most Recent Command ******************#
        self.row += 1
        self.command_layout = QGridLayout()
    # label
        self.recent_command_label = QLabel("Command Log")
        self.recent_command_label.setFixedHeight(30)
#         print("Label height: {}".format(self.recent_command_label.height()))
        self.command_layout.addWidget(self.recent_command_label,0,0,alignment=Qt.AlignHCenter)
    # reading
        self.most_recent_command = QTextEdit()
#         self.most_recent_command.setEnabled(False) 
#                 #(prevents you from accidentally typing in the box, but also removes scrolling)
        self.command_layout.addWidget(self.most_recent_command,1,0)
#         self.most_recent_command.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.most_recent_command.setMaximumWidth(500)
        self.most_recent_command.setMinimumWidth(300)
        self.most_recent_command.setFixedHeight(int(self.TEXT_HEIGHT*8))
#     # timestamp
#         self.recent_command_time = QTextEdit()
#         self.command_layout.addWidget(self.recent_command_time,1,1,alignment=Qt.AlignLeft)
#         self.recent_command_time.setFixedHeight(self.TEXT_HEIGHT)
    # layout
        self.output_layout.addLayout(self.command_layout,self.row,0,1,0)
        self.row += 1 # for the graph
        
        
#**************** Actions Log ******************#
#         self.row += 1
#         self.action_layout = QGridLayout()
    # label
        self.action_layout = QGridLayout()
        self.recent_action_label = QLabel("Actions Log")
        self.recent_action_label.setFixedHeight(30)
#         print("Label height: {}".format(self.recent_command_label.height()))
        self.action_layout.addWidget(self.recent_action_label,0,0,alignment=Qt.AlignHCenter)
#         self.output_layout.addWidget(self.recent_action_label,1,3,alignment=Qt.AlignHCenter)
    # reading
        self.most_recent_action = QTextEdit()
        self.action_layout.addWidget(self.most_recent_action,1,0)
        self.most_recent_command.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.most_recent_action.setMaximumWidth(500)
        self.most_recent_action.setMinimumWidth(300)
#         self.most_recent_action.setFixedHeight(int(self.TEXT_HEIGHT*8))
        
        self.layout.addLayout(self.output_layout,0,0)
#         self.layout.addLayout(self.action_layout,0,1)
#     # timestamp
#         self.recent_command_time = QTextEdit()
#         self.command_layout.addWidget(self.recent_command_time,1,1,alignment=Qt.AlignLeft)
#         self.recent_command_time.setFixedHeight(self.TEXT_HEIGHT)
    # layout
#         self.output_layout.addLayout(self.action_layout,self.row,0,1,0)
#         self.row += 1 # for the graph
        
#**************** Status Bar ******************#
#     # setup
#         self.progress_widget = QWidget()
#         self.progress_layout = QHBoxLayout(self.progress_widget)
#         self.output_layout.addWidget(self.progress_widget,self.row,0,1,0)
#     # label 0%
#         lab0 = QLabel("0%")
#         self.progress_layout.addWidget(lab0,alignment=Qt.AlignRight)
#     # slider
#         self.progress = QSlider(Qt.Horizontal,parent=self)
# #         self.progress = QProgressBar(parent=self)
#         self.progress_layout.addWidget(self.progress)
#     # setup
#         self.progress.setMinimum(0)
#         self.progress.setMaximum(100)
#         self.progress.setEnabled(False)
#         self.progress.setFixedHeight(30)
#         self.progress.setMaximumWidth(640)
#     # label 100%
#         lab100 = QLabel("100%")
#         self.progress_layout.addWidget(lab100,alignment=Qt.AlignLeft)
#         self.progress_widget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)

#         self.row += 1

# #         self.blank = QLabel("")
# #         self.blank.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
# #         self.output_layout.addWidget(self.blank,self.row,0)       
        
# #         self.row += 1
