import sys
import time
import threading
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Basic functions

########## Input and printing ##################################

def pr(text): # print but with no carriage return
    print(text, end='')

########### NUMBER FORMATTING: Str->Num, Sig Figs ###################

def to_num(string): ##############################
    # convert a string to a number
        # int if an integer
        # float if a decimal
        # np.nan if not a number
    try:
        n = float(string)
    except:
        return np.nan
    if n % 1 == 0:
        return int(n)
    return n


def sigfigs1(n, figs=2): ##############################
    # round to significant figures
    # if it's one significant figure which would be 1, it goes to 2 sig figs
    if n < 0: # if negative, make positive but remember to reverse later
        neg = True
        n *= -1
    else: neg = False
        
    if n == 0: # to avoid logarithm errors
        return 0
    try:
        log_remainder = (np.log(n)/np.log(10)%1)
    except: 
        return 0
    starts_with_1 = log_remainder < (np.log(2)/np.log(10)%1)
    if starts_with_1 and figs==1:
        figs = 2
        
    digits = np.floor(np.log(n)/np.log(10))+1
    rounded = np.round(n, figs - int(digits))
    if neg:
        rounded *= -1
    return rounded

########### TIME FORMATTING #########################################

def gt(): ##############################
    # Returns the time since the beginning of the epoch,
    # but only as many digits as ##,###.### to save space
    # Bad for knowing the absolute time, but more memory-efficient for calculating elapsed time
    return time.time()%100000*1000//1/1000


def timeFormat(s): ##############################
    # convert seconds [int] to min:sec [str]
    text = "{mins:n}:{secs:02.0f}"
    return text.format(mins=s//60,secs=s%60)

def current_time(): ##############################
    # current time as hr:min:sec
    full_t = time.time()
    t = time.localtime(full_t)
    [h, m, s] = t[3:6]
    ampm = " am"
    if h>12:
        h = h % 12
        ampm = " pm"
    fracs = (full_t*100%100//1)
    text = "{hrs:n}:{mins:02n}:{secs:02.0f}.{fracs:02n}"
    return text.format(hrs=h,mins=m,secs=s,fracs=fracs)+ampm

########### XLSX AND DICT FORMATTING ################################
    
def excelFormat(string): ##############################
    """ 
    Function: Adds .xlsx to the end of a string if it doesn't already end in .xlsx
    Purpose: Otherwise, if you click on a file [name].xlsx to save a new version of it,
    the new version would be [name].xlsx.xlsx instead of [name].xlsx 
    """
    if string[-5:]==".xlsx":
        return string
    return string + ".xlsx"

def print_dict(dictionary): ##############################
    # Prints a dictoinary as "key   item \n"
    # Works best in a fixed-width font
    # Used for printing new parameters after a change
    l = 0
    message = ""
    for i in dictionary:
        if len(i)>l:
            l = len(i)
    for i in dictionary:
        for j in range(l-len(i)+2):
            message += ' '
        message += i
        message += ": "
        message += str(dictionary[i])
        message += '\n'
    return(message)

########### THREADING ###############################################
    
# runs a thread and returns the output
# delays what comes below it
def thread_return(f,*args): ##############################
#     thread_return_value = 0
    def myf(*args):
        global thread_return_value
        thread_return_value = f(*args)        
    loop = threading.Thread(target=myf, args=args)
    loop.start()
    loop.join()
    return thread_return_value

# runs a thread
# doesn't delay what comes below it (unless wait=True)
def thread_do(f, args=(), wait=False):   ##############################  
    loop = threading.Thread(target=f, args=args)
    loop.start()
    if wait:
        loop.join()

########### DATAFRAME NAVIGATION ########################################
# For DataFrame df, returns the value of r_col
# in the first row where s_col = s_val
def myloc(df,s_col,s_val, r_col):
    return df.loc[df[s_col]==s_val].iloc[0][r_col]

# For the DataFrame df, returns the value of r_col in the ith row
def myiloc(df,i, r_col):
    return df.iloc[i][r_col]
        
########### MISCELLANEOUS ###############################################

# A horizontal separator between sections        
def HSeparator():
    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    separator.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
    separator.setLineWidth(1)
    return separator

def VSeparator():
    separator = QFrame()
    separator.setFrameShape(QFrame.VLine)
    separator.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
    separator.setLineWidth(1)
    return separator
    
# Not actually sure if this is different from time.sleep()
def mysleep(t): ##############################
    def simple_sleep(t):
        t0 = time.time()
        while time.time()<t0+t:
            pass
    loop = threading.Thread(target=simple_sleep, args=[t])
    loop.start()
    loop.join()
    
# There can't be multiple QApplications at once, so this function opens one but makes sure it's the only one
def start_QApplication():
    if not QApplication.instance():
        return QApplication(sys.argv)
        # return QApplication([]) 
            # if there's no chance of command-line arguments
    else:
        return QApplication.instance()
    
# Creates a message box saying that there was an invalid input
def invalid_input():    
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("At least one input\nwas not valid")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()