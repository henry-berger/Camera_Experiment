from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from main_interface import Interface

# The window containing the GUI
class GUI(QMainWindow):
    resized = pyqtSignal() # the signal if the window is resized
    
    def __init__(self, params, parent=None):        
        super(GUI, self).__init__(parent) # initialize
        self.do_close = False
        self.setWindowTitle("CCD Experiment GUI") # set title
        
        # add an PumpInterface, which contains all the other widgets
        self.widget = Interface(self, params=params) 
        self.setCentralWidget(self.widget) 
        
    # The function that can actually close the window
    def myclose(self):
        self.do_close = True
        self.close()
        
    """
    I want to prompt the user if they close when there are unsaved data. 
    The easiest way is to force the user to click a custom exit button, not the x.
    Therefore, this disables the X button, requiring myclose() to be called.
    """
    def closeEvent(self, event): 
        if self.do_close: # i.e., if myclose has been called
            event.accept()
        elif self.widget.exit():
            event.accept()
        else:
            event.ignore()

#         else:  
#             # explain what's happening
# #             msg = QMessageBox()
# #             msg.setIcon(QMessageBox.Information)
# #             msg.setText("Please use the Exit button to close")
# #             msg.setStandardButtons(QMessageBox.Ok)
# #             msg.exec()
#             event.ignore()
#             self.widget.exit()
            
            
    # send a signal whenever the window is resized (for resizing the image)
    def resizeEvent(self, event):
        self.resized.emit()
        return super(GUI, self).resizeEvent(event)