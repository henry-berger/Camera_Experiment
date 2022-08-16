import os
import numpy as np
import pyvisa 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

sys.path.append('../')
import utils
import actions

# the popup to make a custom action
class Custom_Action_Popup(QDialog):

    def __init__(self, parent, 
                 type_to_add, # "pump" or "collect"
                 action=None, # the Pump_Action or Collect_Action to edit
                 index=-1 # The index of the action to be edited
                ):        
        
        super(Custom_Action_Popup, self).__init__(parent)
        
        self.p = parent.p # the main window (Interface object)
        self.parent = parent # the custom popup (Custom_Run_Popup object)

        
        self.add_type=type_to_add
        self.action = action
        self.index=index 

        self.init_vars()
        self.init_UI()
        
    def init_vars(self):
        
        self.WIDTH = 210
        self.SMALL_WIDTH = 100
        
#         self.defaults = self.p.default_params

        # the current default parameters
        self.current_params = self.p.current_params
        # current_params doesn't include pump numbers, so I add them locally here
        self.current_params['in_pump'] = "Pump 1"
        self.current_params['out_pump'] = "None"
        
        # If it's an edit, not a creation, get the parameters for that action
        if not self.action==None:
            if self.add_type=="pump":
                self.current_params = {'volume'  : self.action.volume,
                                       'v_units' : self.action.v_units,
                                       'rate'    : self.action.rate,
                                       'r_units' : self.action.r_units,
                                       'in_pump' : self.action.in_pump,
                                       'out_pump': self.action.out_pump
                                      }
            if self.add_type=="collect":
                self.current_params = {'other time int'   : self.action.tint,
                                       'other total time' : self.action.ttot,
                                       'other time mult'  : self.action.tmult
                                      }
        
        
    def init_UI(self):
        self.setWindowTitle("Set Parameters")
        self.layout = QGridLayout(self)
        row = 0
        col = 0
        
#######################################################################################################
######################## PUMP SETUP ###################################################################
#######################################################################################################

        if self.add_type == "pump":

    #************************ Pump Number **************************#
        # label
            label = QLabel("Infusing Pump:")
            self.layout.addWidget(label,row,col,alignment=Qt.AlignHCenter)
    #         label.setFixedWidth(self.WIDTH)
        # dropdown
            self.pump_dropdown = QComboBox()
            pump_options = ["Pump 1","Pump 2","Pump 3"]
            self.pump_dropdown.addItems(pump_options)
            self.pump_dropdown.setCurrentIndex(pump_options.index(self.current_params['in_pump']))
        # layout
            self.layout.addWidget(self.pump_dropdown,row+1,col)
            self.pump_dropdown.setFixedWidth(self.WIDTH)

            col += 1

            self.layout.addWidget(utils.VSeparator(),row,col,2,1)

            col += 1

    #************************ Volume **************************#
        # label
            label = QLabel("Volume (mL):")
            self.layout.addWidget(label,row,col,1,2,alignment=Qt.AlignHCenter)
    #         label.setFixedWidth(self.WIDTH)
    #     input
            self.volume_edit = QLineEdit()
            self.volume_edit.setText(str(self.current_params['volume']))
#             if self.action
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
            rate_options = ["mL/min","mL/hr","uL/hr"]
            self.r_units.addItems(rate_options)
            self.r_units.setCurrentIndex(['MM',"MH","UH"].index(self.current_params['r_units']))

        # layout
            self.layout.addWidget(self.r_units,row+1,col+1,alignment=Qt.AlignHCenter)
            self.r_units.setFixedWidth(self.SMALL_WIDTH)

            col += 2

            self.layout.addWidget(utils.VSeparator(),row,col,2,1)

            col += 1

    #************************ Reciprocating Pump Number **************************#
        # label
            label = QLabel("Withdrawing Pump:")
            self.layout.addWidget(label,row,col,alignment=Qt.AlignHCenter)
    #         label.setFixedWidth(self.WIDTH)
        # dropdown
            self.r_pump_dropdown = QComboBox()
            r_pump_options=["None","Pump 1","Pump 2","Pump 3"]
            self.r_pump_dropdown.addItems(r_pump_options)
            try:
                self.r_pump_dropdown.setCurrentIndex(r_pump_options.index(self.current_params['out_pump']))
            except:
                self.r_pump_dropdown.setCurrentIndex(r_pump_options.index("None"))
        # layout
            self.layout.addWidget(self.r_pump_dropdown,row+1,col)
            self.r_pump_dropdown.setFixedWidth(self.WIDTH)

            row += 2
            
##################################################################################################
######################## COLLECTION SETUP ########################################################
##################################################################################################
        
        elif self.add_type == "collect":
        
            self.clabel = QLabel("Collection")
            self.layout.addWidget(self.clabel,row,0,1,10,alignment=Qt.AlignHCenter)
            self.clabel.setFont(QFont('Arial', 10))
            self.clabel.setFixedHeight(32)

            row += 1

            col = 0
            
    #************************ Collection Rate **************************#
        # label
            label = QLabel("Collection every...")
            self.layout.addWidget(label,row,col,1,2,alignment=Qt.AlignHCenter)
    #         label.setFixedWidth(self.WIDTH)
    #     input
            self.int_edit = QLineEdit()
            self.int_edit.setText(str(self.current_params['other time int']))
        # layout
            self.layout.addWidget(self.int_edit,row+1,col,alignment=Qt.AlignHCenter)
            self.int_edit.setFixedWidth(self.SMALL_WIDTH)
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
            self.t_total_edit = QLineEdit()
            self.t_total_edit.setText(str(self.current_params['other total time']))
        # layout
            self.layout.addWidget(self.t_total_edit,row+1,col,alignment=Qt.AlignHCenter)
            self.t_total_edit.setFixedWidth(self.SMALL_WIDTH)
        # input
            self.t_tot_units = QLabel("s")
#             self.t_tot_units.addItems(["s","times"])
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
            self.multiplier_edit.setText(str(self.current_params['other time mult']))
        # layout
            self.layout.addWidget(self.multiplier_edit,row+1,col,alignment=Qt.AlignHCenter)
            self.multiplier_edit.setFixedWidth(self.SMALL_WIDTH)


            row += 2

            self.layout.addWidget(utils.HSeparator(),row,0,1,10)

            row += 1
        
        
######################## GO BUTTON ###############################################################
    
    
    # button
        if self.action==None:
            self.set_btn = QPushButton("Add Action")
        else:
            self.set_btn = QPushButton("Confirm Edits")
        self.set_btn.clicked.connect(self.add_actions)
        self.set_btn.setAutoDefault(True)
    # layout
        self.layout.addWidget(self.set_btn,row,0,1,10)
        self.set_btn.setStyleSheet("background-color: tan;") 

    
    def add_actions(self, reset=False): ##########################################################
#         print("executed")
######################## PUMP ACTION ###############################################################

        if self.add_type == "pump":

            # Get the values
            vol = utils.to_num(self.volume_edit.text())
            rate = utils.to_num(self.rate_edit.text())
            v_units = self.volume_units.currentText()
            r_units = self.r_units.currentText()
            pump = self.pump_dropdown.currentText()
            r_pump = self.r_pump_dropdown.currentText()
            if r_pump == "None":
                r_pump = None
        
            pump_key = {"Pump 1":0,"Pump 2":1,"Pump 3":2,"None":None}
            r_units_key = {"mL/min":"MM","mL/hr":"MH","uL/hr":"UH"}
            v_units_key = {"mL":"ML","uL":"UL"}
            
            # Check for invalid input
            if np.isnan([vol, rate]).any() or min([vol, rate])<=0 or pump == r_pump: 
                utils.invalid_input()
                return # to avoid doing any more of the actions below
            
            # create a pump action
            pa = actions.Pump_Action(volume=vol,
                                     v_units = v_units_key[v_units],
                                     rate=rate,
                                     r_units = r_units_key[r_units],
                                     in_pump=pump,
                                     out_pump=r_pump
                                     )
            if self.index==-1: # i.e., it's a creation, not an edit
                self.parent.add_action(pa)
            else:
                self.parent.edit_action(pa,self.index)
            self.close()
            return
        
######################## COLLECT ACTION ###############################################################

        elif self.add_type=="collect":
            
            # try to get all the values
            tint  = utils.to_num(self.int_edit.text())
            ttot  = utils.to_num(self.t_total_edit.text())
            tmult = utils.to_num(self.multiplier_edit.text())
            
            if np.isnan([tint, ttot, tmult]).any() or min([tint,ttot, tmult])<=0:     # or is negative
                utils.invalid_input()
                return
            
            # create a collect action
            ca = actions.Collect_Action(\
                                        tint=tint,
                                        ttot=ttot,
                                        tmult=tmult)
            if self.index==-1: # i.e., it's a creation, not an edit
                self.parent.add_action(ca)
            else:
                self.parent.edit_action(ca,self.index)            
            
            self.close()
            return