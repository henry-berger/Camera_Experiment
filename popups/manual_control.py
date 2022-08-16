import os
import numpy as np
import pyvisa 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

sys.path.append('../')
import utils

class Manual_Control_Popup(QDialog):

    def __init__(self, parent):        
        super(Manual_Control_Popup, self).__init__(parent)
        self.p = parent # the overall window
        self.init_vars()
        self.init_UI()
        
    def init_vars(self): #############################################################################################
        self.do_close = False # default: don't close unless "Confirm" is pressed
        
        self.WIDTH = 210
        self.SMALL_WIDTH = 100
        
        self.current_params = self.p.current_params

        self.DEFAULT_RATE = 360
        self.DEFAULT_VOLUME = 1
        self.DEFAULT_TOTAL_TIME = 10
        self.DEFAULT_TIME_INT = 1
        self.DEFAULT_MULT = 1
        
        
    def init_UI(self): #############################################################################################
        self.setWindowTitle("Manual Pump Control")
        self.layout = QGridLayout(self)
        row = 0
        col = 0
        
############################################################################################################################################
######################## PUMP CONTROL ######################################################################################################
############################################################################################################################################

        self.plabel = QLabel("Pumps")
        self.layout.addWidget(self.plabel,row,0,1,10,alignment=Qt.AlignHCenter)
        self.plabel.setFont(QFont('Arial', 10))
        self.plabel.setFixedHeight(32)
        
        row += 1


#************************ Pump Number **************************#
    # label
        label = QLabel("Infusing Pump:")
        self.layout.addWidget(label,row,col,alignment=Qt.AlignHCenter)
#         label.setFixedWidth(self.WIDTH)
    # dropdown
        self.pump_dropdown = QComboBox()
        self.pump_dropdown.addItems(["Pump 1","Pump 2","Pump 3"])
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
        self.volume_units.setCurrentIndex(['MM','MH','UH'].index(self.current_params['r_units']))

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
        self.r_pump_dropdown.addItems(["None","Pump 1","Pump 2","Pump 3"])
    # layout
        self.layout.addWidget(self.r_pump_dropdown,row+1,col)
        self.r_pump_dropdown.setFixedWidth(self.WIDTH)
                
        row += 2
        
        self.layout.addWidget(utils.HSeparator(),row,0,1,10)
        
        row += 1
        
############################################################################################################################################
######################## COLLECTION ########################################################################################################
############################################################################################################################################
        
    
        self.clabel = QLabel("Collection")
        self.layout.addWidget(self.clabel,row,0,1,10,alignment=Qt.AlignHCenter)
        self.clabel.setFont(QFont('Arial', 10))
        self.clabel.setFixedHeight(32)
        
        row += 1
        col = 0

        self.reset_btn = QPushButton("Prep for New Run")
        self.layout.addWidget(self.reset_btn,row,col,alignment=Qt.AlignRight)
        self.reset_btn.setCheckable(False) # button can stay down
        self.reset_btn.clicked.connect(self.p.reset)
        self.reset_btn.setStyleSheet("background-color: white;")
        self.reset_btn.setFixedWidth(self.WIDTH)
        
        self.abort_btn = QPushButton("Abort")
        self.layout.addWidget(self.abort_btn,row+1,col,alignment=Qt.AlignLeft)
        self.abort_btn.setCheckable(False) # button can stay down
        self.abort_btn.clicked.connect(self.p.abort)
        self.abort_btn.setStyleSheet("background-color: red;")
        self.abort_btn.setFixedWidth(self.WIDTH)
        
        col += 2
    
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
        self.layout.addWidget(label,row+1,col+1,alignment=Qt.AlignHCenter)
        
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
#         self.t_tot_units.addItems(["s","times"])
    # layout
        self.layout.addWidget(self.t_tot_units,row+1,col+1,alignment=Qt.AlignHCenter)
        self.t_tot_units.setFixedWidth(self.SMALL_WIDTH)
        
        col += 2
        
        self.layout.addWidget(utils.VSeparator(),row,col,2,1)
        
        col += 1
        
        
#************************ Pump Number **************************#
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
        
        
############################################################################################################################################
######################## FUNCTIONS #########################################################################################################
############################################################################################################################################
        
#************************ Go Button **************************#
    # button
        self.go_btn = QPushButton("Pump")
        self.go_btn.clicked.connect(self.ex)
    # layout
        self.layout.addWidget(self.go_btn,row,0,1,4)
        self.go_btn.setStyleSheet("background-color: pink;")
        
    # button
        self.collect_btn = QPushButton("Collect")
        self.collect_btn.clicked.connect(self.collect)
    # layout
        self.layout.addWidget(self.collect_btn,row,5,1,4)
        self.collect_btn.setStyleSheet("background-color: pink;") 
        
        row += 1
        
    # button
        self.collect_btn = QPushButton("Pump and Collect")
        self.collect_btn.clicked.connect(self.ex)
    # layout
        self.layout.addWidget(self.collect_btn,row,2,1,5)
        self.collect_btn.setStyleSheet("background-color: pink;") 
        
        
        row += 1
        
        self.message = QLabel("")
        self.layout.addWidget(self.message,row,0,1,10)

    
    def ex(self): #############################################################################################
#         print("executed")
        vol = utils.to_num(self.volume_edit.text())
        v_units = self.volume_units.currentText()
        rate = utils.to_num(self.rate_edit.text())
        r_units = self.r_units.currentText()
        pump = self.pump_dropdown.currentText()
        r_pump = self.r_pump_dropdown.currentText()
        
        pump_key = {"Pump 1":0,"Pump 2":1,"Pump 3":2}
        r_units_key = {"mL/min":"MM","mL/hr":"MH","uL/hr":"UH"}
        v_units_key = {"mL":"ML","uL":"UL"}

        if np.isnan(vol * rate) or rate<0 or pump==r_pump:
            text = "Invalid motor control command"
        else:
            text = "Moved {} by {} {} at {} {}, opposite {}".format(pump, vol, v_units, rate, r_units, r_pump)
            
            if r_pump == "None":
                self.p.ps.pump(p=pump_key[pump], 
                               volume=vol, 
                               rate=rate, 
                               v_units = v_units_key[v_units],
                               r_units = r_units_key[r_units])
            else:
                
                self.p.ps.exchange(inf=pump_key[pump], 
                                   wdr=pump_key[r_pump],
                                   volume=vol, 
                                   rate=rate, 
                                   v_units = v_units_key[v_units],
                                   r_units = r_units_key[r_units])
            
            
        self.message.setText(text)
        self.p.display_command(text)
        
        
    def collect(self): #############################################################################################
#         print("executed")
        t_tot = utils.to_num(self.t_total_edit.text())
        t_int = utils.to_num(self.int_edit.text())
        t_mult = utils.to_num(self.multiplier_edit.text())

        if np.isnan(t_tot * t_int*t_mult) or min(t_tot,t_int,t_mult)<0:
            text = "Invalid motor control command"
        else:
            text = "Collect for {tt} s, every {ti} s, with multiplier {tm}".format(
                tt=t_tot, 
                ti=t_int, 
                tm=t_mult)
            
            
            
            self.p.collect(on=True, 
                          total_time = t_tot, 
                          data_period=t_int,
                          period_multiplier = t_mult)
            
            
        self.message.setText(text)
        self.p.display_command(text)