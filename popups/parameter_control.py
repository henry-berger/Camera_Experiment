import os
import numpy as np
import pyvisa 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyflycap2.interface import GUI as cam_GUI # Camera setup GUI


import sys
sys.path.append('../')
import utils

class Parameter_Popup(QDialog):

    def __init__(self, parent):        
        super(Parameter_Popup, self).__init__(parent)
        self.p = parent # the overall window
        self.init_vars()
        self.init_UI()
        
    def init_vars(self):
        self.do_close = False # default: don't close unless "Confirm" is pressed
        
        self.WIDTH = 210
        self.SMALL_WIDTH = 100
        
        self.defaults = self.p.default_params
        self.current_params = self.p.current_params
        
        
    def init_UI(self):
        self.setWindowTitle("Set Default Parameters")
        self.layout = QGridLayout(self)
        row = 0
        col = 0
        
############################################################################################################################################
######################## PUMP PARAMETERS ###################################################################################################
############################################################################################################################################

        self.plabel = QLabel("Pumps")
        self.layout.addWidget(self.plabel,row,0,1,10,alignment=Qt.AlignHCenter)
        self.plabel.setFont(QFont('Arial', 10))
        self.plabel.setFixedHeight(32)
        
        row += 1


        col = 2
        
#************************ Volume **************************#
    # label
        label = QLabel("Volume (mL):")
        self.layout.addWidget(label,row,col,1,2,alignment=Qt.AlignHCenter)
#         label.setFixedWidth(self.WIDTH)
#     input
        self.volume_edit = QLineEdit()
        self.volume_edit.setText(str(self.current_params['volume']))
    # layout
        self.layout.addWidget(self.volume_edit,row+1,col,alignment=Qt.AlignHCenter)
        self.volume_edit.setFixedWidth(self.SMALL_WIDTH)
    # input
        self.volume_units = QComboBox()
        self.volume_units.addItems(["mL","uL"])
        self.volume_units.setCurrentIndex(['ML','UL'].index(self.current_params['v_units']))
    # layout
        self.layout.addWidget(self.volume_units,row+1,col+1,alignment=Qt.AlignHCenter)
        self.volume_units.setFixedWidth(self.SMALL_WIDTH)
        
        col += 2
        
        self.layout.addWidget(utils.VSeparator(),row,col,2,1)
    
        col += 1
        
#************************ Rate **************************#
    # label
        label = QLabel("Rate (mL):")
        self.layout.addWidget(label,row,col,1,2,alignment=Qt.AlignHCenter)
#         label.setFixedWidth(self.WIDTH)
#     input
        self.rate_edit = QLineEdit()
        self.rate_edit.setText(str(self.current_params['rate']))
    # layout
        self.layout.addWidget(self.rate_edit,row+1,col,alignment=Qt.AlignHCenter)
        self.rate_edit.setFixedWidth(self.SMALL_WIDTH)
    # input
        self.r_units = QComboBox()
        self.r_units.addItems(["mL/min","mL/hr","uL/hr"])
        self.r_units.setCurrentIndex(['MM',"MH","UH"].index(self.current_params['r_units']))
        
    # layout
        self.layout.addWidget(self.r_units,row+1,col+1,alignment=Qt.AlignHCenter)
        self.r_units.setFixedWidth(self.SMALL_WIDTH)
                
        row += 2
        col = 2
        
        self.layout.addWidget(utils.HSeparator(),row,0,1,10)
        
        row += 1
        
############################################################################################################################################
######################## COLLECTION PARAMETERS #############################################################################################
############################################################################################################################################
    
        self.clabel = QLabel("Collection")
        self.layout.addWidget(self.clabel,row,0,1,10,alignment=Qt.AlignHCenter)
        self.clabel.setFont(QFont('Arial', 10))
        self.clabel.setFixedHeight(32)
        
        row += 1
        
######################## TARGET SOLUTION ################################################################################################

        
        col = 0
    
        self.tlabel = QLabel("After adding the\ntarget solution")
        self.layout.addWidget(self.tlabel,row,col,2,2,alignment=Qt.AlignRight)
        self.tlabel.setFont(QFont('Arial', 9))
        
        col += 2
    
#************************ Collection Rate **************************#
    # label
        label = QLabel("Collection every...")
        self.layout.addWidget(label,row,col,1,2,alignment=Qt.AlignHCenter)
#         label.setFixedWidth(self.WIDTH)
#     input
        self.int_edit = QLineEdit()
        self.int_edit.setText(str(self.current_params['target time int']))
    # layout
        self.layout.addWidget(self.int_edit,row+1,col,alignment=Qt.AlignHCenter)
        self.int_edit.setFixedWidth(self.SMALL_WIDTH)
    # input
        label= QLabel("s")
    # layout
        self.layout.addWidget(label,row+1,col+1,alignment=Qt.AlignLeft)
        
        col += 2

        self.layout.addWidget(utils.VSeparator(),row,col,2,1)
    
        col += 1
    
#************************ Collection interval **************************#
    # label
        label = QLabel("Stop after ...")
        self.layout.addWidget(label,row,col,1,2,alignment=Qt.AlignHCenter)
#         label.setFixedWidth(self.WIDTH)
#     input
        self.t_total_edit = QLineEdit()
        self.t_total_edit.setText(str(self.current_params['target total time']))
    # layout
        self.layout.addWidget(self.t_total_edit,row+1,col,alignment=Qt.AlignHCenter)
        self.t_total_edit.setFixedWidth(self.SMALL_WIDTH)
    # input
        self.t_tot_units = QLabel("s")
#         self.t_tot_units.addItems(["s","times"])
    # layout
        self.layout.addWidget(self.t_tot_units,row+1,col+1,alignment=Qt.AlignHCenter)
        self.t_tot_units.setFixedWidth(self.SMALL_WIDTH)
        
        col += 2
        
        self.layout.addWidget(utils.VSeparator(),row,col,2,1)
        
        col += 1
        
        
#************************ Time Multiplier **************************#
    # label
        label = QLabel("Time multiplier")
        self.layout.addWidget(label,row,col,alignment=Qt.AlignHCenter)
#         label.setFixedWidth(self.WIDTH)
    # dropdown
        self.multiplier_edit = QLineEdit()
        self.multiplier_edit.setText(str(self.current_params['target time mult']))
    # layout
        self.layout.addWidget(self.multiplier_edit,row+1,col,alignment=Qt.AlignHCenter)
        self.multiplier_edit.setFixedWidth(self.SMALL_WIDTH)
        
        
        row += 2
                
        self.layout.addWidget(utils.HSeparator(),row,2,1,8)
        
        row += 1
        
        
######################## OTHER SOLUTIONS ################################################################################################

        col = 0
    
        self.olabel = QLabel("After adding any\nother solution")
        self.layout.addWidget(self.olabel,row,col,2,2,alignment=Qt.AlignRight)
        self.olabel.setFont(QFont('Arial', 9))
        
        col += 2
    
#************************ Collection Rate **************************#
    # label
        label = QLabel("Collection every...")
        self.layout.addWidget(label,row,col,1,2,alignment=Qt.AlignHCenter)
#         label.setFixedWidth(self.WIDTH)
#     input
        self.oint_edit = QLineEdit()
        self.oint_edit.setText(str(self.current_params['other time int']))
    # layout
        self.layout.addWidget(self.oint_edit,row+1,col,alignment=Qt.AlignHCenter)
        self.oint_edit.setFixedWidth(self.SMALL_WIDTH)
    # input
        label= QLabel("s")
#         self.r_units.addItems(["mL/min","mL/hr","uL/hr"])
    # layout
        self.layout.addWidget(label,row+1,col+1,alignment=Qt.AlignLeft)
        
        col += 2

        self.layout.addWidget(utils.VSeparator(),row,col,2,1)
    
        col += 1
    
#************************ Collection interval **************************#
    # label
        label = QLabel("Stop after ...")
        self.layout.addWidget(label,row,col,1,2,alignment=Qt.AlignHCenter)
#         label.setFixedWidth(self.WIDTH)
#     input
        self.ot_total_edit = QLineEdit()
        self.ot_total_edit.setText(str(self.current_params['other total time']))
    # layout
        self.layout.addWidget(self.ot_total_edit,row+1,col,alignment=Qt.AlignHCenter)
        self.ot_total_edit.setFixedWidth(self.SMALL_WIDTH)
    # input
        self.ot_tot_units = QLabel("s")
#         self.ot_tot_units.addItems(["s","times"])
    # layout
        self.layout.addWidget(self.ot_tot_units,row+1,col+1,alignment=Qt.AlignHCenter)
        self.ot_tot_units.setFixedWidth(self.SMALL_WIDTH)
        
        col += 2
        
        self.layout.addWidget(utils.VSeparator(),row,col,2,1)
        
        col += 1
        
        
#************************ Time Multiplier********************#
    # label
        label = QLabel("Time multiplier")
        self.layout.addWidget(label,row,col,alignment=Qt.AlignHCenter)
#         label.setFixedWidth(self.WIDTH)
    # dropdown
        self.omultiplier_edit = QLineEdit()
        self.omultiplier_edit.setText(str(self.current_params['other time mult']))
    # layout
        self.layout.addWidget(self.omultiplier_edit,row+1,col,alignment=Qt.AlignHCenter)
        self.omultiplier_edit.setFixedWidth(self.SMALL_WIDTH)
        
        
        row += 2
        
        self.layout.addWidget(utils.HSeparator(),row,0,1,10)
        
        row += 1
        
        
######################## GO BUTTON ################################################################################################
    
    # button
        self.camera_btn = QPushButton("Camera Setup")
        self.camera_btn.clicked.connect(self.set_up_camera)
        self.camera_btn.setAutoDefault(False)
    # layout
        self.layout.addWidget(self.camera_btn,row,0,1,1)
        self.camera_btn.setStyleSheet("background-color: lightgray;") 
    
    # button
        self.set_btn = QPushButton("Set Parameters")
        self.set_btn.clicked.connect(self.set_all_params)
        self.set_btn.setAutoDefault(True)
    # layout
        self.layout.addWidget(self.set_btn,row,2,1,5)
        self.set_btn.setStyleSheet("background-color: tan;") 
        
    # button
        self.reset_btn = QPushButton("Reset to defaults")
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        self.reset_btn.setAutoDefault(False)
    # layout
        self.layout.addWidget(self.reset_btn,row,8,1,2)
        self.reset_btn.setStyleSheet("background-color: lightgray;") 
        
        row += 1
        
        self.note = QLabel(\
"Note: The default run is as follows:\n\
1. Collect (other solution parameters)\n\
2. Inject from pump 1\n\
3. Collect (other solution parameters)\n\
4. Inject from pump 2, withdraw from pump 1\n\
5. Collect (other solution parameters)\n\
6. Inject from pump 3, withdraw from pump 2\n\
7. Collect (target solution parameters)\n\
8. Inject from pump 2, withdraw from pump 3\n\
9. Collect (other solution parameters)\n\
10. Inject from pump 1, withdraw from pump 2\n\
11. Collect (other solution parameters)\
")
        self.layout.addWidget(self.note,row,0,1,10,alignment=Qt.AlignHCenter)
  
        
        row += 1
        
        self.message = QLabel("")
        self.message.setFont(QFont('Courier', 9))
        self.layout.addWidget(self.message,row,0,1,10,alignment=Qt.AlignHCenter)
        
############################################################################################################################################
######################## COLLECTION PARAMETERS #############################################################################################
############################################################################################################################################

    
    def set_all_params(self, reset=False): #############################################################################################
#         print("executed")
        v_units_key = {"mL": "ML", "uL":"UL"}
        r_units_key = {"mL/min":"MM", "mL/hr":"MH","uL/hr":"UH"}
    
        # try to get all the values
        vol     = utils.to_num(self.volume_edit.text())
        v_units = v_units_key[self.volume_units.currentText()]
        r_units = r_units_key[self.r_units.currentText()]
        rat     = utils.to_num(self.rate_edit.text())
        tint    = utils.to_num(self.int_edit.text())
        ttot    = utils.to_num(self.t_total_edit.text())
        tmult   = utils.to_num(self.multiplier_edit.text())
        oint    = utils.to_num(self.oint_edit.text())
        otot    = utils.to_num(self.ot_total_edit.text())
        omult   = utils.to_num(self.omultiplier_edit.text())

        # CHECK IF IT'S A RESET
        if reset:
            [vol,v_units,rat,r_units,tint,ttot,tmult,oint,otot,omult] = self.defaults.values() 
            message = "Resetting.\n"
            main_message = "Reset parameters"
            
        # CHECK FOR INVALID INPUTS
        elif np.isnan(vol*rat*tint*ttot*tmult*oint*otot*omult):
            message = "Warning: following invalid input(s)\nwere ignored:\n"
            self.current_params = self.p.current_params
            current_vals = list(self.current_params.values())
            keys = list(self.current_params.keys())
            # undo any invalid ones
            vs=[vol,rat,tint,ttot,tmult,oint,otot,omult]
            for i in range(len(vs)):
                if np.isnan(vs[i]):
                    vs[i]=current_vals[i]
                    message += "\t- "+ keys[i]+"\n"
            [vol,rat,tint,ttot,tmult,oint,otot,omult]=vs
        else:
            message = ""
#             [vol,rat,tint,ttot,tmult,oint,otot,omult] = self.current_params.values()

        # ACTUALLY CHANGE THE VALUES
        # change the values
        self.p.set_all_params(vol,v_units,
                              rat,r_units,
                              tint,ttot,tmult,
                              oint,otot,omult)
        
        # DISPLAY THE CHANGES
        main_message = "Changed parameters:\n\tnone, "
        current_vals = list(self.current_params.values())
        keys = list(self.current_params.keys())
        vs=[vol,v_units,rat,r_units,tint,ttot,tmult,oint,otot,omult]
        # add any changed parameter to the list of changes
        for i in range(len(vs)):
            if not vs[i]==current_vals[i]: # if the value has been changed
                main_message +=  keys[i]+ " to " + str(vs[i]) + ", "
                main_message = main_message.replace("none, ","")
        main_message = main_message[:-2]   # to remove the ", " at the end
        
        # print the mes
        message += "Set variables as follows:\n"
        # make sure this popup registers the change, then redraw
        self.current_params = self.p.current_params
        self.redraw()
        # print the parameters
        message = message + utils.print_dict(self.current_params)
        message += "\n"
        message += "Time-stamp: " + utils.current_time()
        self.message.setText(message) # in the set_parameters window
        self.p.display_command(main_message,show=True) # in the main window
        
    def reset_to_defaults(self): #############################################################################################
        self.set_all_params(reset=True)
        
    def redraw(self): #############################################################################################
        self.current_params = self.p.current_params
    # pumps
        self.volume_edit.setText(str(self.current_params['volume']))
        self.volume_units.setCurrentIndex(['ML','UL'].index(self.current_params['v_units']))
        self.rate_edit.setText(str(self.current_params['rate']))
        self.r_units.setCurrentIndex(['MM',"MH","UH"].index(self.current_params['r_units']))
    # target solution
        self.int_edit.setText(str(self.current_params['target time int']))
        self.t_total_edit.setText(str(self.current_params['target total time']))
        self.multiplier_edit.setText(str(self.current_params['target time mult']))
    # other solution
        self.oint_edit.setText(str(self.current_params['other time int']))
        self.ot_total_edit.setText(str(self.current_params['other total time']))
        self.omultiplier_edit.setText(str(self.current_params['other time mult']))
        
    def set_up_camera(self): #############################################################################################
        gui = cam_GUI()
        gui.show_selection()