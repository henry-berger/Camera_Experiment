import os
import numpy as np
import pyvisa 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from popups.custom_action import Custom_Action_Popup

import sys
sys.path.append('../')
import utils
import actions

# the popup to choose the ports for the instruments
class Custom_Run_Popup(QDialog):
    def __init__(self, parent):        
        super(Custom_Run_Popup, self).__init__(parent)
        self.p = parent # the overall window
        self.init_vars()
        self.init_UI()
        
    def init_vars(self):
        
        self.action_list = [] # list of all actions in the custom run
        
        self.WIDTH = 210 # default width for buttons
        self.SMALL_WIDTH = 60 # width for edit buttons
        
        self.current_params = self.p.current_params # the current parameters 
    
    
    def init_UI(self): # initialize the user interface
        
    # setup
        self.setWindowTitle("Set Custom Run")
        self.layout = QGridLayout(self)
        row = 0
        col = 0
        
        self.plabel = QLabel("Custom Run")
        self.layout.addWidget(self.plabel,row,0,1,2,alignment=Qt.AlignHCenter)
        self.plabel.setFont(QFont('Arial', 10))
        self.plabel.setFixedHeight(32)
        row += 1
        
        label = QLabel(\
"Note:\n\
The program will wait for a collect action to finish\n\
before starting the next action, but will not wait\n\
after a pump action.\n\n\
Therefore, you must ensure there is sufficient\n\
waiting time between successive pumps.\n\n\
If you just want a pause, you can do a collection\n\
where total time is shorter than collection rate.\
")
        self.layout.addWidget(label,row,0,1,2,alignment=Qt.AlignHCenter)
        
        row += 1
        
    # add buttons
        self.add_collect = QPushButton("+ Collection")
        self.layout.addWidget(self.add_collect,row,0,alignment=Qt.AlignRight)
        self.add_collect.clicked.connect(self.set_collect) # opens a Custom_Action_Popup
        
        self.add_pump = QPushButton("+ Pump")
        self.layout.addWidget(self.add_pump,row,1,alignment=Qt.AlignLeft)
        self.add_pump.clicked.connect(self.set_pump) # opens a Custom_Action_Popup
        
    # the layout with a list of all the actions (starts empty)
        row += 1
        self.command_layout = QGridLayout(self)
        self.layout.addLayout(self.command_layout,row,0,1,2)
        
    # run button
        row += 1
        self.run_custom = QPushButton("Run")
        self.run_custom.setEnabled(False) # it will be enabled once an action is added
        self.run_custom.setStyleSheet("background-color: lightgreen;")
        self.layout.addWidget(self.run_custom,row,0,1,2,alignment=Qt.AlignHCenter)
        # I think clicked.connect can't have arguments, hence this extra function
        def parent_run():
            self.p.run(self.action_list)
        self.run_custom.clicked.connect(parent_run)
        
        row += 1
        
        label = QLabel(\
"You can save using the button on the main window.\n\
However, if you exit, you will have to reenter all the \n\
actions if you want to run it again.\
")
        self.layout.addWidget(label,row,0,1,2,alignment=Qt.AlignHCenter)

        
    # Redraws the list of commands every time something is changed
    def redraw(self):
    # clear the layout, so there aren't duplicates
        for i in reversed(range(self.command_layout.count())): 
            self.command_layout.itemAt(i).widget().setParent(None)
            
        # Adds a printout of each action, plus an edit button
        for i in range(len(self.action_list)):
            
            # label with a description of the command
            label=QLabel(self.action_list[i].print_command())
            self.command_layout.addWidget(label,i,0,alignment=Qt.AlignLeft)
        
            # edit button
            button = QPushButton("Edit")
            self.command_layout.addWidget(button,i,1,alignment=Qt.AlignLeft)
            button.clicked.connect(self.edit_action_maker(i))
            button.setFixedWidth(self.SMALL_WIDTH)
            
        # now that there's at least one action, enable the run button
        self.run_custom.setEnabled(True)


    # add a new pump action
    def set_pump(self):
        self.custom_action_popup = Custom_Action_Popup(self, "pump")
        self.custom_action_popup.show() 
        
    # add a new collect action
    def set_collect(self):
        self.custom_action_popup = Custom_Action_Popup(self, "collect")
        self.custom_action_popup.show() 
        
    # makes a function to edit an action
    # i is the index of the action to be edited
    def edit_action_maker(self, i):
        
        a = self.action_list[i] # the action
        
        if type(a)==actions.Pump_Action:
            typ = "pump"
        elif type(a)==actions.Collect_Action:
            typ = "collect"
            
        def edit_action_function():        
            self.custom_action_popup = Custom_Action_Popup(parent=self,
                                                           type_to_add=typ, 
                                                           action=a,
                                                           index=i  )
            self.custom_action_popup.show() 
            
        return edit_action_function
        
    # add an action to the list, and redraw
    # to be called by the adding popup
    def add_action(self,action):
        self.action_list.append(action)
        self.redraw()
        
    # edit an action to the list, and redraw
    # to be called by the editing popup
    def edit_action(self, action, i):
        self.action_list[i]=action
        self.redraw()
#         self.commands.setText(self.commands.text()+"\n"+action.print_command())