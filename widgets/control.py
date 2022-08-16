from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyflycap2.interface import GUI as cam_GUI # Camera setup GUI

import sys
sys.path.append('../')
import popups


# the widget with all the buttons:
class Control_Widget(QWidget):
    def __init__(self,parent):
        super(Control_Widget, self).__init__(parent)
#         print("Made")
        self.p = parent # the pump interface, with all the functions
        self.BUTTON_WIDTH = 180
        self.init_UI()
        
    def init_UI(self):
        
        self.control_widget = QWidget()
        self.control_layout = QGridLayout(self.control_widget)
        
       
        row = 0 # the row
    
#         Separator = QFrame()
#         Separator.setFrameShape(QFrame.HLine)
#         Separator.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
#         Separator.setLineWidth(1)
#         Separator.setFixedHeight(2)
#         self.control_layout.addWidget(Separator,row,0,1,0)
        
#         row += 1
        
        self.elabel = QLabel("Control")
        self.control_layout.addWidget(self.elabel,row,0,1,0,alignment=Qt.AlignHCenter)
        self.elabel.setFont(QFont('Arial', 10))
        self.elabel.setMaximumHeight(36)
        
        row += 1

        # Run button
        self.run_btn = QPushButton("Default Run")
        self.control_layout.addWidget(self.run_btn,row,0,alignment=Qt.AlignRight)
        self.run_btn.setCheckable(False) # button can stay dow
        self.run_btn.clicked.connect(self.p.run)
        self.run_btn.setStyleSheet("background-color: lightgreen;")
        self.run_btn.setFixedWidth(int(self.BUTTON_WIDTH))
        
        self.set_cstm = QPushButton("Custom Run")
        self.control_layout.addWidget(self.set_cstm,row,1,alignment=Qt.AlignLeft)
        self.set_cstm.setStyleSheet("background-color: yellow;")
        self.set_cstm.clicked.connect(self.set_custom)
        self.set_cstm.setFixedWidth(int(self.BUTTON_WIDTH))
        
        row += 1
        
        self.set_params_btn = QPushButton("Adjust Defaults")
        self.control_layout.addWidget(self.set_params_btn,row,0,alignment=Qt.AlignRight)
        self.set_params_btn.setStyleSheet("background-color: tan;")
        self.set_params_btn.clicked.connect(self.set_params)
        self.set_params_btn.setFixedWidth(self.BUTTON_WIDTH)
            
        
        self.man_ctrl = QPushButton("Manual Control")
        self.control_layout.addWidget(self.man_ctrl,row,1,alignment=Qt.AlignLeft)
        self.man_ctrl.setStyleSheet("background-color: magenta;")
        self.man_ctrl.clicked.connect(self.manual_pump_control)
        self.man_ctrl.setFixedWidth(int(self.BUTTON_WIDTH))
        
        row += 1

#         # Run button
#         self.crun_btn = QPushButton("Custom Run")
#         self.control_layout.addWidget(self.crun_btn,row,0,alignment=Qt.AlignRight)
#         self.crun_btn.setCheckable(False) # button can stay down
# #         self.crun_btn.clicked.connect(self.p.run)
#         self.crun_btn.setStyleSheet("background-color: yellow;")
#         self.crun_btn.setFixedWidth(int(self.BUTTON_WIDTH))
        

        
        row += 1
        
        self.camera_btn = QPushButton("Configure Camera")
        self.control_layout.addWidget(self.camera_btn,row,0,alignment=Qt.AlignLeft)
        self.camera_btn.setCheckable(False) # button can stay down
        self.camera_btn.clicked.connect(self.set_up_camera)
        self.camera_btn.setStyleSheet("background-color: gray;")
        self.camera_btn.setFixedWidth(self.BUTTON_WIDTH)
        
        self.reset_btn = QPushButton("Prep for New Run")
        self.control_layout.addWidget(self.reset_btn,row,1,alignment=Qt.AlignLeft)
        self.reset_btn.setCheckable(False) # button can stay down
        self.reset_btn.clicked.connect(self.p.reset)
        self.reset_btn.setStyleSheet("background-color: white;")
        self.reset_btn.setFixedWidth(self.BUTTON_WIDTH)
        
        row += 1
        
        # Graph button
        self.graph_btn = QPushButton("Plot")
        self.control_layout.addWidget(self.graph_btn,row,0,alignment=Qt.AlignRight)
        self.graph_btn.setCheckable(True) # button can stay down
        self.graph_btn.clicked.connect(self.p.graph)
        self.graph_btn.setStyleSheet("background-color: lightblue;")
        self.graph_btn.setFixedWidth(self.BUTTON_WIDTH)
        
        # Graph button
        self.abort_btn = QPushButton("Abort")
        self.control_layout.addWidget(self.abort_btn,row,1,alignment=Qt.AlignLeft)
        self.abort_btn.setCheckable(False) # button can stay down
        self.abort_btn.clicked.connect(self.p.abort)
        self.abort_btn.setStyleSheet("background-color: red;")
        self.abort_btn.setFixedWidth(self.BUTTON_WIDTH)
    
        row += 1
            
        # Run button
        self.collect_btn = QPushButton("Data Collection")
#         self.control_layout.addWidget(self.collect_btn,row,0,alignment=Qt.AlignRight)
#         self.collect_btn.setCheckable(True) # button can stay down
#         self.collect_btn.clicked.connect(self.p.collect_button_signal)
#         self.collect_btn.setStyleSheet("background-color: lightgreen;")
#         self.collect_btn.setFixedWidth(self.BUTTON_WIDTH)
        
        
        # Run button

        
#         row += 1
        
#         # Run button
#         self.reset_btn = QPushButton("Prep for New Run")
#         self.control_layout.addWidget(self.reset_btn,row,0,alignment=Qt.AlignRight)
#         self.reset_btn.setCheckable(False) # button can stay down
#         self.reset_btn.clicked.connect(self.p.reset)
#         self.reset_btn.setStyleSheet("background-color: white;")
#         self.reset_btn.setFixedWidth(self.BUTTON_WIDTH)
        
        # Zero button
#         self.zero_btn = QPushButton("Current Pos = 0")
#         self.control_layout.addWidget(self.zero_btn,row,1,alignment=Qt.AlignLeft)
#         self.zero_btn.setCheckable(False) # button can stay down
#         self.zero_btn.clicked.connect(self.p.set_current_to_0)
#         self.zero_btn.setStyleSheet("background-color: white;")
#         self.zero_btn.setFixedWidth(self.BUTTON_WIDTH)

        row += 1

        # Exit button
        self.exit_btn = QPushButton("Exit")
        self.control_layout.addWidget(self.exit_btn,row,1,alignment=Qt.AlignLeft)
        self.exit_btn.setCheckable(False)  # button can't stay down
        self.exit_btn.clicked.connect(self.p.exit)     
        self.exit_btn.setStyleSheet("background-color: red;")
        self.exit_btn.setFixedWidth(self.BUTTON_WIDTH)
        
#************************ Save Buttons **************************#
        
        # Save buttons
        self.save_layout = QHBoxLayout()
        # Auto-save Checkbox
        self.auto_save_btn = QPushButton("Auto \u2014")
        self.auto_save_btn.setFixedWidth(int(self.BUTTON_WIDTH/2))  
        self.auto_save_btn.setCheckable(True)   # button can't stay down
        self.auto_save_btn.clicked.connect(self.p.auto_save)
        self.auto_save_btn.setStyleSheet("background-color: lightgray;")
#         self.auto_save_btn.setLayoutDirection(Qt.RightToLeft)
        self.save_layout.addWidget(self.auto_save_btn)
        
        # save button
        self.save_btn = QPushButton("Save")
        self.save_layout.addWidget(self.save_btn)
        self.save_btn.setCheckable(False)   # button can't stay down
        self.save_btn.clicked.connect(self.p.save)
        self.save_btn.setStyleSheet("background-color: lightgray;")
        self.save_btn.setFixedWidth(int(self.BUTTON_WIDTH/2))    
        
        self.save_layout.setSpacing(0)
        self.control_layout.addLayout(self.save_layout,row,0,alignment=Qt.AlignRight)
        
        
    def manual_pump_control(self):
        self.mpc_popup = popups.Manual_Control_Popup(self.p)
        self.mpc_popup.show() 
        
    def set_params(self):
        self.param_popup = popups.Parameter_Popup(self.p)
        self.param_popup.show() 
        
    def set_custom(self): 
        self.custom_run_popup = popups.Custom_Run_Popup(self.p)
        self.custom_run_popup.show() 

    def set_up_camera(self): #############################################################################################
        gui = cam_GUI()
        gui.show_selection()
