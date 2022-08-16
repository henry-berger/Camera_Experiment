import os
import numpy as np
import pyvisa 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

sys.path.append('../')
import utils

class Initial_Setup_Popup(QDialog):

    def __init__(self, parent):         
        super(Initial_Setup_Popup, self).__init__(parent)
        self.p = parent # the overall window
        self.do_close = False # default: don't close unless "Confirm" is pressed
        self.setWindowTitle("Setup")
        # find which ports exist
        self.rm = pyvisa.ResourceManager()
        self.port_list = self.rm.list_resources()
        
        self.init_UI() # create the user interface
        
    def init_UI(self):
        self.layout = QGridLayout(self)
        row = 0

# The dropdowns aren't connected to any functions, 
# because they will be read when the popup is closed.  
        
#************************ Syringe Port Seleciton *****************************************#
    # label
        self.syringe_port_label = QLabel("Syringe Port Name:")
        self.layout.addWidget(self.syringe_port_label,row,0,alignment=Qt.AlignRight)
    # dropdown
        self.syringe_port_dropdown = QComboBox()
        self.syringe_port_dropdown.addItems(self.port_list)
        self.syringe_port_dropdown.addItems(["None"]) # if chosen, will create a fake syringe
    # layout
        self.layout.addWidget(self.syringe_port_dropdown,row,1)
        self.syringe_port_dropdown.setMaximumWidth(200)

        
# This isn't necessary, because the script finds the camera automatically
#         row += 1
# #************************ CCD Port **************************************************#
#     # label
#         self.CCD_port_label = QLabel("CCD Port Name:")
#         self.layout.addWidget(self.CCD_port_label,row,0,alignment=Qt.AlignRight)
#     # dropdown
#         self.CCD_port_dropdown = QComboBox()
#         self.CCD_port_dropdown.addItems(["None"])
#         self.CCD_port_dropdown.addItems(self.port_list)
#     # layout
#         self.layout.addWidget(self.CCD_port_dropdown,row,1)
#         self.CCD_port_dropdown.setMaximumWidth(200)

#************************ Autosave  **************************************************#

        row += 1

    # label
        self.auto_save_label = QLabel("Auto-save as: ")   
        self.layout.addWidget(self.auto_save_label,row,0, alignment = Qt.AlignRight)
        self.auto_save_label.setMaximumHeight(20)


    # Current file label
        self.file_name_label = QLabel(os.getcwd()+"\Most_Recent_Data.xlsx")
        self.layout.addWidget(self.file_name_label,row,1,alignment = Qt.AlignRight)
                # Shouldn't be necessary because it is read at the end
    # set button
        self.set_auto_save = QPushButton("Set")
        self.set_auto_save.clicked.connect(self.choose_save_file)
        self.set_auto_save.setCheckable(False)   # button can't stay down
        self.set_auto_save.setAutoDefault(False)

    # layout
        row += 1
        self.set_auto_save.setFixedWidth(50)
        self.layout.addWidget(self.set_auto_save,row,1,alignment = Qt.AlignRight)
        
        
#************************ Syringe Diameters  ***************************************#
        row += 1        
    # label
        self.s1dl = QLabel("Syringe\nDiameters:")
        self.s1dl.setFixedWidth(150)
        self.layout.addWidget(self.s1dl,row,0,alignment=Qt.AlignRight)      
        self.slayout = QGridLayout()
    # dropdown
        self.s1d = QLineEdit()
        self.s1d.setText("5")
        self.slayout.addWidget(self.s1d,0,1)
        self.s1d.setMaximumWidth(80)
        
        self.s2d = QLineEdit()
        self.s2d.setText("5")
        self.slayout.addWidget(self.s2d,1,1)
        self.s2d.setMaximumWidth(80)
        
        self.s3d = QLineEdit()
        self.s3d.setText("5")
        self.slayout.addWidget(self.s3d,2,1)
        self.s3d.setMaximumWidth(80)
        
        
        labels = ["Buffer","Buffer:DDM","Buffer:DDM:Target"]
        for i in range(3):
            lab = QLabel(labels[i])
            lab.setMaximumWidth(200)
            self.slayout.addWidget(lab,i,0)  
            
            mlab = QLabel(" mm")
            mlab.setMaximumWidth(50)
            self.slayout.addWidget(mlab,i,2,alignment=Qt.AlignLeft)  
        
        self.layout.addLayout(self.slayout,row,1,alignment=Qt.AlignLeft)    
        self.slayout.setSpacing(0)
        row += 1
        self.layout.addWidget(utils.HSeparator(),row,0,1,0)

        
#************************ Instructions  ********************************************#

        row += 1
        self.instructions = QLabel("Please follow the following instructions for each pump:\n\n\
        1. Turn the pump on. If you hold the right-most arrow\n\twhile turning the machine on, the pump is reset.\n\n\
        2. Hold the Diameter button until the menu comes up.\n\n\
        3. Keep hitting the Diameter button until you see \"AD:00\"\n\n\
        4. Hit the left-most up arrow to switch to \"Addr\" (Address mode)\n\n\
        5. Use the right-most up arrows to set the pump addresses as follows:\n\
            a. Buffer solution: Pump 0\n\
            b. Modified buffer solution: Pump 1\n\
            c. Sample solution: Pump 2\n\n\
        6. Hit the Diameter button once or twice more, \n\t until you see the baud rate, which defaults to 1920.\n\n\
        7. Hit any of the arrows until the baud rate is 9600.\n\n\
        8. Connect the \"To Computer\" port of Pump 1 to the computer.\n\
        9. Connect the \"To Computer\" port of Pump 2 to the \"To Network\" port of Pump 1.\n\
        10. Connect the \"To Computer\" port of Pump 3 to the \"To Network\" port of Pump 2.\n\n\
        (If you had't done all of this already, you might need to rerun the Python script.)")
        self.instructions.setWordWrap(True)
        self.instructions.setFont(QFont('Segoe Ui', 9))

        self.layout.addWidget(self.instructions,row,0,1,0, alignment = Qt.AlignHCenter)
        
#************************ Donfirm Button  ********************************************#
        row += 1
        self.ok_btn = QPushButton("Confirm")
        self.ok_btn.setStyleSheet("background-color: lightgreen;")
        self.layout.addWidget(self.ok_btn,row,1)
        self.ok_btn.clicked.connect(self.myclose) # the function that actually closes the window
        self.ok_btn.setFixedWidth(120)
        self.ok_btn.setAutoDefault(True)

        
#************************ Functions  *********************************************#

    # the function to actually close
    def myclose(self):
        self.do_close = True
    # pass the ports and file name to the main window
        self.p.set_syringe_port(self.syringe_port_dropdown.currentText())
#         self.p.set_CCD_port(self.CCD_port_dropdown.currentText())
        self.p.set_save_file_name(self.file_name_label.text())
        self.diameters = [utils.to_num(self.s1d.text()),
                          utils.to_num(self.s2d.text()),
                          utils.to_num(self.s3d.text())
                         ]
        # Make sure everything is a valid number
        if np.isnan(self.diameters).any():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("At least one syringe diameter\nwas not a valid number")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        else:
            self.p.set_diameters(self.diameters)
            self.close()

        
    def closeEvent(self, event):
        if self.do_close: # i.e., if myclose has been called
            event.accept()
        else: # i.e., if the x button has been pressed
            # (don't exit)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Please click the Confirm button instead")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            event.ignore()
            
    def choose_save_file(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("Excel files (*.xlsx)")
        if dlg.exec():
            filename = dlg.selectedFiles()[0] # the filename the user selects
            self.save_file_name = utils.excelFormat(filename)
            self.file_name_label.setText(self.save_file_name)
#             self.p.set_save_file_name(self.save_file_name)
                # Shouldn't be necessary because it is read at the end