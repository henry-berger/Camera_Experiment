from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np
import pandas as pd
import sys # for making the popups
import threading # to do multiple loops at once
import matplotlib.pyplot as plt # for plotting

import utils
import popups
import instruments

class Interface(QWidget): 

#####################################################################################################################################
##********************** Initialize ***********************************************************************************************##
#####################################################################################################################################

    def __init__(self, parent, params):  
        print(utils.gt())
    # basic initialize
        super(Interface, self).__init__(parent) # initialize
        self.window = parent
#     Prompt the user for the names of the ports
        self.popup = popups.Initial_Setup_Popup(self)
        self.popup.exec()   
    # create the electrometer and translation stage objects
        self.CCD = instruments.CCD.CCD(parent=self)
        self.ps = instruments.multi_suringe.All_Pumps(port=self.syringe_port, parent=self,diameters=self.diameters)
    # full initialize
        self.init_vars()
        self.init_general_UI()
        
    def init_vars(self): #############################################################################################
    # data
        self.data = pd.DataFrame({'t': [], 'pics' : [], 'liquid' : [],'run' : []})
        self.saved = True
        self.auto_save_on = False
        self.running=False
        self.pics = []
    # first time for things
        self.first_collection = True # whether a t0 has already been established
        self.first_graphing = True # if the graph has to be initialized
        self.last_event = 0 # essentially forever ago
        self.last_collection = 0 # essentially forever ago
        self.run_number = 1
        self.last_pump_event = 0
#         self.CCD_start_time = 0
    # running parameters
        self.scan_distance = 10
        self.wait_time = 1.5
        self.measure_time = 3
        self.ssd = 0.5
    # running parameter defaults
        self.scan_distance_DEFAULT = self.scan_distance
        self.wait_time_DEFAULT = self.wait_time
        self.measure_time_DEFAULT = self.measure_time
        self.ssd_DEFAULT = self.ssd
        
        self.default_params = params
        
        
        self.current_params = self.default_params.copy()
        
        self.set_all_params(*self.current_params.values())
        
        
    def set_all_params(self,
                       vol,v_units,
                       rat, r_units,
                       tint,ttot,tmult,
                       oint,otot,omult): #############################################################################################
#         self.pump_vol = vol
#         self.pump_v_units = v_units
#         self.pump_rate = rat
#         self.pump_r_units = r_units
#         self.target_int = tint
#         self.target_tot = ttot
#         self.target_mult = tmult
#         self.other_int = oint
#         self.other_tot = otot
#         self.other_mult = omult
        
        self.current_params = {'volume'            : vol,
                               'v_units'           : v_units,
                               'rate'              : rat,
                               'r_units'           : r_units,
                               'target time int'   : tint,
                               'target total time' : ttot,
                               'target time mult'  : tmult,
                               'other time int'    : oint,
                               'other total time'  : otot,
                               'other time mult'   : omult,
                        }
        
    
    
    # initialize the UI
    def init_general_UI(self): 
    # general layout
        self.layout = QGridLayout(self)
        self.layout.setRowStretch(2,1)
    # input layout (params and control)
        self.input_layout = QGridLayout(self)
        self.layout.addLayout(self.input_layout,0,0)      
#     # parameter layout
#         self.pw = Parameter_Widget(self)
#         self.input_layout.addWidget(self.pw.param_widget,0,1) 

    # buffers on the sides
#         blank1 = QLabel("")
#         blank1.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
#         blank2 = QLabel("")
#         blank2.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
#         self.input_layout.addWidget(blank1,0,0)       
#         self.input_layout.addWidget(blank2,0,4)       

        
    # control layout
        self.cw = Control_Widget(self)
        self.input_layout.addWidget(self.cw.control_widget,0,1)    
        
        self.input_layout.addWidget(VSeparator(),0,2)       

        
    # output layout
        self.ow = Output_Widget(self)
        self.ow.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.input_layout.addWidget(self.ow.output_widget,0,3)  
        
        self.layout.addWidget(HSeparator(),1,0)       
        
        self.pw = Plot_Widget(self)
        self.pw.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.layout.addWidget(self.pw.plot_widget,2,0)       

        


#************************** Setter functions for the popup ****************************************#
        
    # Functions that the popup window uses to change the stage and electrometer port names
    def set_syringe_port(self, port):
        self.syringe_port = port
        
    def set_CCD_port(self, port):
        self.CCD_port = port
        
    def set_save_file_name(self, name):
        self.save_file_name = name
        
    def set_diameters(self, diameters):
        self.diameters = diameters


#####################################################################################################################################
##********************** Run/Abort ************************************************************************************************##
#####################################################################################################################################
    
    def run(self, actions=None):
        self.display_command("Run started",show=True)
        print(actions)
#         self.pw.progress.setValue(0)
        self.cw.run_btn.setText("Running...")
#         self.cw.graph_btn.setChecked(True)
#         self.graph()
        self.cw.run_btn.setEnabled(False)
        self.cw.collect_btn.setEnabled(False)
        if len(self.data['run']>0):
            self.run_number = int(max(self.data['run']))+1
        else:
            self.run_number = 1
        # start the data collection loop
        print(actions)
        def crl():
            self.custom_run_looper(actions)
        self.run_loop = threading.Thread(target=crl)
        self.abort_now = False
        self.run_loop.start()
#         self.run_looper()
          
    def abort(self): #############################################################################################
#         print(self.running)
        self.cw.graph_btn.setChecked(False)
        self.graph()
        if self.running:
            self.abort_now = True
            self.data_end_now = True
            try:
                self.data_loop.join() 
            except:
                print("Couldn't end loop")
                
        self.ps.stop_all()
#             self.cw.abort_btn.setEnabled(False)
#             self.cw.abort_btn.setCheckable(True)
#             self.cw.abort_btn.setChecked(True)
#             self.display_command("Aborting...")


#     def run_looper(self):
# #         1) Start the CCD recording with prefunctionalized patterned chip under buffer 
# #             (maybe 10 frames at 1 frame per second for baseline)

#         def post_movement_pause():
#             print("TIME: {}".format(self.CCD.time()))
# #             pass
# #             mysleep(1)

#         self.running = True
#         self.collect(on=True,total_time=self.other_tot,
#                      data_period=self.other_int,
#                      period_multiplier=self.other_mult  
#                     )
#         self.data_loop.join()
#         self.display_action("Data collection period ended")
#         if self.auto_save_on:
#             self.compile_and_save()
#         if self.check_for_abort(): return
        
# #         2) Inject buffer (pump #1) and record while the system settles (another 10 frames at 1 frame per second?)
#         self.display_action("Pump 1 (Buffer) Injected")
#         self.ps.pump(0)
#         post_movement_pause()
#         self.collect(on=True,total_time=self.other_tot,
#                      data_period=self.other_int,
#                      period_multiplier=self.other_mult  
#                     )
#         self.data_loop.join()
#         self.display_action("Data collection period ended")
#         if self.auto_save_on:
#             self.compile_and_save()
#         if self.check_for_abort(): return
        
# #         3) Inject DDM:buffer (pump #2) and record while the system settles (another 10 frames at 1 frame per second?)
#         self.display_action("Pump 2 (DDM:Buffer) Injected")
#         self.ps.exchange(inf=1,wdr=0)
#         post_movement_pause()
#         self.collect(on=True,total_time=self.other_tot,
#                      data_period=self.other_int,
#                      period_multiplier=self.other_mult  
#                     )
                     
#         self.data_loop.join()
#         self.display_action("Data collection period ended")
#         if self.auto_save_on:
#             self.compile_and_save()
#         if self.check_for_abort(): return

# #         4) Inject target:DDM:buffer (pump #3). Record logarithmically (i.e. a few frames at 1 sec, 3 sec, 
# #             10 sec, 30 sec, 100 sec, 300 sec, 1000 sec) for a while.
# #             (the idea is to get out the dynamics without filling up computer memory)

#         self.display_action("Pump 3 (target:DDM:Buffer) Injected")
#         self.ps.exchange(inf=2,wdr=1);
#         post_movement_pause()
#         self.collect(on=True,total_time=self.target_tot,
#                      data_period=self.target_int,
#                      period_multiplier=self.target_mult    
#                     )
#         self.data_loop.join()
#         self.display_action("Data collection period ended")
#         if self.auto_save_on:
#             self.compile_and_save()
#         if self.check_for_abort(): return

# #         5) Inject DDM:buffer (pump #2) until signal stabilizes (?10 sec)
#         self.display_action("Pump 2 (DDM:Buffer) Injected")
#         self.ps.exchange(inf=1,wdr=2);
#         post_movement_pause()
#         self.collect(on=True,total_time=self.other_tot,
#                      data_period=self.other_int,
#                      period_multiplier=self.other_mult  
#                     )
#         self.data_loop.join()
#         self.display_action("Data collection period ended")
#         if self.auto_save_on:
#             self.compile_and_save()
#         if self.check_for_abort(): return

# #         6) Inject buffer (pump #1) to rinse off DDM until signal stabilizes (?10 sec).
        
#         self.display_action("Pump 1 (Buffer) Injected")
#         self.ps.exchange(inf=0,wdr=1);
#         post_movement_pause()
#         self.collect(on=True,total_time=self.other_tot,
#                      data_period=self.other_int,
#                      period_multiplier=self.other_mult  
#                     )
#         self.data_loop.join()
#         self.display_action("Data collection period ended")
#         if self.auto_save_on:
#             self.compile_and_save()
#         if self.check_for_abort(): return
    
# #         6) Exit

#         self.abort_now = True
#         if self.check_for_abort(): 
#             self.reset()
#             self.display_command("Run ended.")
#             return

    def check_for_abort(self):
        if self.abort_now:
            self.abort()
            self.cw.run_btn.setText("Run")
            self.cw.run_btn.setEnabled(True)
            self.cw.collect_btn.setEnabled(True)
#             self.pw.progress.setValue(0)
            self.display_command("Run aborted")
            self.cw.abort_btn.setEnabled(True)
            self.cw.abort_btn.setCheckable(False)
            self.cw.abort_btn.setChecked(False)
            self.running = False
        return self.abort_now
    
    
    def default_actions_list(self):
        default_collect = Collect_Action(ttot  = self.current_params['other total time'],
                                         tint  = self.current_params['other time int'],
                                         tmult = self.current_params['other time mult'])
        
        target_collect  = Collect_Action(ttot  = self.current_params['target total time'],
                                         tint  = self.current_params['target time int'],
                                         tmult = self.current_params['target time mult'])
        
        def default_pump(p_1, p_2):
            return Pump_Action(volume   = self.current_params['volume'],
                               v_units  = self.current_params['v_units'],
                               rate     = self.current_params['rate'],
                               r_units  = self.current_params['r_units'],
                               in_pump  = p_1, 
                               out_pump = p_2
            )

        actions = [

            default_collect,  
            default_pump("Pump 1", None),
            default_collect,
            default_pump("Pump 2", "Pump 1"),
            default_collect,
            default_pump("Pump 3", "Pump 2"),
            target_collect,
            default_pump("Pump 2", "Pump 3"),
            default_collect,
            default_pump("Pump 1", "Pump 2"),
            default_collect                
        ]
        
        return actions
            
        
    def custom_run_looper(self, actions=None):
#         print(actions)
        if actions==None or actions == False:
            actions = self.default_actions_list()
        
        def post_movement_pause():
            # mysleep(1) # would pause for a second
            print("TIME: {}".format(self.CCD.time()))

        self.running = True
    
   
        def execute(action):
            if type(action)==Pump_Action:
                pump_keys = {"Pump 1": 0,
                             "Pump 2": 1,
                             "Pump 3": 2,
                             "None"  : None,
                              None   : None}
                
                pump_names = {"Pump 1": "Pump 1 (Buffer)",
                              "Pump 2": "Pump 2 (DDM:Buffer)",
                              "Pump 3": "Pump 3 (target:DDM:Buffer)"}
                
                print(action)
                if action.out_pump == None: # If it's just an infusion
                    self.ps.pump(p       = pump_keys[action.in_pump],
                                 volume  = action.volume,
                                 rate    = action.rate, 
                                 v_units = action.v_units,
                                 r_units = action.r_units
                                )
                else: # if it's an exhange
                    self.ps.exchange(inf     = pump_keys[action.in_pump],
                                     wdr     = pump_keys[action.out_pump],
                                     volume  = action.volume,
                                     rate    = action.rate, 
                                     v_units = action.v_units,
                                     r_units = action.r_units
                                    )
                
                post_movement_pause()
                self.display_action(pump_names[action.in_pump] + " Injected.",show=True)
            
            else: # If it's a collect action
                self.collect(on=True,
                             total_time        = action.ttot,
                             data_period       = action.tint,
                             period_multiplier = action.tmult
                            )
                self.data_loop.join()
                self.display_action("Data collection period ended",show=False)
                
                
            if self.auto_save_on and (type(action)==Collect_Action):
                self.compile_and_save()
            
    
#         print(type(actions))
        for action in actions:
            execute(action)
            if self.check_for_abort(): return

        self.abort_now = True
        if self.check_for_abort(): 
            self.display_command("Run ended.",show=True)
            self.reset()
            return

#####################################################################################################################################
##********************** Data Collection ******************************************************************************************##
#####################################################################################################################################

    def time_since(self, t):
        return t - self.last_pump_event

    def collect_data(self):
#         t = gt()
#         tinit = current_time()
        
#         pr("Getting status...")
        self.sval =  self.ps.status # get data
#         pr("Getting tval...")
#         self.t1 = self.CCD.time()
        pr("Getting picture...")
        self.pic, self.dims, [self.t1, self.t2] =  self.CCD.take_picture()
#         self.pic, self.dims, [self.t1, self.t2] =  [[1,2],[3,4]],[2,2],[gt(), gt()] #self.CCD.take_picture()
#         self.pic, self.dims, [self.t1, self.t2] =  [[1,2],[3,4]],[2,2],[5,6] #self.CCD.take_picture()

#         pr("Getting tval...")
#         self.t2 = self.CCD.time()
        self.tval = (self.t1 + self.t2)/2
        self.t_since = self.tval - self.last_pump_event
#         self.t_since = self.time_since(self.tval) #- self.last_pump_event
#         print("tval: {}\nlpe: {}\nstart: {}".format(self.tval, self.last_pump_event, self.CCD_start_time))
#         pr("Recording data...")
        self.data = self.data.append([{'t':self.tval, 
                                       't1':self.t1,
                                       't2':self.t2,
                                       't_since':self.t_since,
                                       'status':self.sval, 
                                       'run':self.run_number, 
                                       'dims':self.dims}], 
                                     ignore_index = True) # append data 
#         pr("Appending picture...")
        self.pics.append(self.pic)
#         pr("Done with collection...")
        print()#"t={}, dt={}".format(np.round(self.tval,3), np.round(self.t2-self.t1),3))
#         pr("Last collection...")
        self.last_collection = gt()
#         tint = np.round(gt()-t,2)
#         print("Displaying...")
#         self.display_action("Collection (took {} s)".format(tint),t=tinit)
#         print("Displayed")
        
#     def collect_data(self):
#         print("Collection at " + current_time() + ' - ',end='')
#         self.tval,self.sval = self.CCD.time(), self.ps.status # get data
#         self.image, self.vals =  self.CCD.take_picture()
# #         self.yval = self.CCD.getval() # this has to be last because it takes a while, 
#                                                 and otherwise the delay would mess up the z reading
#         self.data = self.data.append([{'t':self.tval,'pics':self.vals, 'status':self.sval, 
#                                         'run':self.run_number}], ignore_index = True) # append data    
#         self.pics.append(self.image)
#         self.last_collection = gt()
#         print(current_time())

    def collect_button_signal(self):
        if self.cw.collect_btn.isChecked():
            self.collect(on=True)
        else:
            self.collect(on=False)
    # running this function starts or ends a data collection loop
    def collect(self,on=False, total_measurements=np.inf, total_time = np.inf, data_period=-1,period_multiplier = 1):
        if on:
#             self.display_command("Data collection turned on")
            self.running = True
            self.cw.collect_btn.setText("Data Collection On")
#             self.window.setWindowTitle("Pump GUI (unsaved)") # for some reason, this causes the program to crash
            self.saved = False
            
            if self.first_collection: # if it's the first time collection has been on, set t0
                self.first_collection = False
                self.CCD.t0 = gt()
                
            # start the data collection loop
            try:
                self.data_loop = threading.Thread(target=lambda: self.data_update(total_measurements,total_time,
                                                                                  data_period,period_multiplier))
                self.data_end_now = False
                self.data_loop.start()
            except:
                print("Couldn't start data loop")
            
        else: # i.e., if data collection has been turned off
            try:
                self.cw.collect_btn.setText("Data Collection Off")
                self.display_command("Data collection turned off")
            except:
                print("Couldn't set text of Data Colletion off")
            self.data_end_now = True
            try:
                self.data_loop.join() 
            except:
                print("Couldn't wait for data loop to end")
    # the data collection loop
#     def data_update(self):
#         last_update = gt()-self.data_period # the -period is so that it starts immediately
#         while not self.data_end_now:
#             if gt()-last_update > self.data_period:
#                 last_update = gt()
#                 self.CCD.collect()
#                 self.saved = False
#                 # display the time and stuff
#                 self.pos_display.setText(str(sigfigs1(self.CCD.y,3))+" V")
#                 self.time_display.setText(timeFormat(self.CCD.t))

    def data_update(self, total_measurements=np.inf, total_time=np.inf,data_period=-1,period_multiplier=1):
        if data_period == -1:
            data_period = self.data_period
        
        print("Data period is {}".format(data_period))
        measurements = 0
        end_time = gt() + total_time
        last_update = gt()-data_period # the -period is so that it starts immediately
        while (not self.data_end_now) and gt()<end_time and measurements < total_measurements:
            if gt()-last_update > data_period:
                if self.data_end_now:
                    break
                last_update = gt()
#                 thread_do(self.collect_data)
                self.collect_data()

                if self.saved:
                    self.saved = False
                measurements += 1
                data_period *= period_multiplier
                self.ow.liquid_display.setText(str(self.ps.get_status()))

#                     self.window.setWindowTitle("Pump GUI*")  # because there are unsaved data 
                # display the time and stuff
#                 self.ow.eread_display.setText(str(sigfigs1(self.yval,3))+" V")
            try:
#                 print(self.tval)
#                 self.ow.time_display.setText(timeFormat(self.tval))
                self.ow.time_display.setText(timeFormat(self.CCD.time()))
            except: pass


#####################################################################################################################################
##********************** Graphing *************************************************************************************************##
#####################################################################################################################################
                
    # running this function starts or ends a graphing loop 
    def graph(self): 
        self.graph_period = self.measure_time+self.wait_time
        if self.cw.graph_btn.isChecked():
            self.cw.graph_btn.setText("Plotting On")
            self.display_command("Plotting turned on")

            if self.first_graphing:
                # initalize the graph
                self.first_graphing = False
                self.graph_widget = Image_Widget(self)
                self.pw.plot_layout.addWidget(self.graph_widget,self.pw.row,0,4,0)
#                 self.graph_widget.setScaledContents(True)
                plt.ioff()
#                 plt.figure(figsize=(10,10))
#                 try:
#                     self.ow.output_layout.removeWidget(self.ow.blank)
#                     self.ow.blank.deleteLater()
#                     self.ow.blank = None
#                 except:
#                     pass

            self.graph_loop = threading.Thread(target=self.graph_update) # A loop for data collection
            self.graph_end_now = False
            self.graph_loop.start()
        else: 
            self.cw.graph_btn.setText("Plotting Off")
            self.display_command("Plotting turned off")

#             self.label.setText(str(round(-1*getval(),3)))
            self.graph_end_now = True
            try:
                self.graph_loop.join() 
            except:
                pass

    def graph_update(self): #############################################################################################
        last_update = 0
        while not self.graph_end_now:
            if self.last_collection-last_update > 0:
                last_update = gt()
# #                 plt.ioff() # in interactive mode, the graph doesn't display until you x out
#                 plt.clf() # clear previous graphs
#                 self.plot_graph()
#         #                 # is there a more elegant way of doing this?
#                 plt.savefig('saved_figure.png')
#                 self.pixmap = QPixmap('saved_figure.png')
#                 image = self.CCD.take_picture()[0]
#                 self.image.save("saved_figure.jpg")
                self.pixmap = QPixmap('Most Recent Photo.jpg')
                self.graph_widget.setMyPixmap(self.pixmap)
                self.graph_widget.myresize()
#                 print("Graphed")


#####################################################################################################################################
##********************** Saving ***************************************************************************************************##
#####################################################################################################################################

    def save(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("Excel files (*.xlsx)")
#         filenames = QStringList()
        
        if dlg.exec():
            filename = dlg.selectedFiles()[0] # the filename the user selects
            self.save_file_name = excelFormat(filename)
            
#             print(filename)
#             self.data.to_excel(self.save_file_name) # adds .xlsx if necessary
            self.compile_and_save()
#             print("Saved as", self.save_file_name)
            # make a note that it's been saved
#             self.window.setWindowTitle("Pump GUI")
            self.saved = True
            self.display_command("Saved as "+str(self.save_file_name),show=True)

#******************* Auto-saving ********************###################################################################
            
    # running this function starts or ends a graphing loop 
    def auto_save(self): 
        if self.cw.auto_save_btn.isChecked():
            self.cw.save_btn.setEnabled(False)
            self.auto_save_loop = threading.Thread(target=self.auto_saver) # A loop for data collection
            self.auto_save_on = True
            self.auto_save_loop.start()
        else: 
            self.cw.save_btn.setEnabled(True)
#             self.label.setText(str(round(-1*getval(),3)))
            self.auto_save_on = False
            self.auto_save_loop.join() 

    def auto_saver(self): #############################################################################################
        last_update = 0
        i = 0
        while self.auto_save_on:
            if self.last_collection-last_update > 0 and not self.saved:
                i += 1
                if i % 3 == 0:
                    last_update = gt()
    #                 self
    #                 self.data.to_excel(self.save_file_name) # adds .xlsx if necessary
                    self.compile_and_save()
                    self.display_action("Saved as "+str(self.save_file_name),show=True)
    #                 self.window.setWindowTitle("Pump GUI")
                    self.saved = True
    
    def compile_and_save(self): #############################################################################################
#         self.sum_data = self.summarize_data()
        Excelwriter = pd.ExcelWriter(self.save_file_name,engine="xlsxwriter")
        self.data['pics']=self.pics
#         self.sum_data.to_excel(Excelwriter, sheet_name="Summary Data",index=False)
        self.data.to_excel(Excelwriter, sheet_name="All Data",index=False)
        Excelwriter.save()
        self.feather_file_name = self.save_file_name.replace(".xlsx",".file")
        self.data.to_feather(self.feather_file_name)
        
    
        
#####################################################################################################################################
##********************** Exiting **************************************************************************************************##
#####################################################################################################################################
        
    # triggered when the exit button is pressed
    def exit(self):
        if not self.saved:
            # ask the user if they want to save
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("You have unsaved data. Are you sure you would like to exit?")
            msg.setInformativeText("If you do, your data will be lost.")
            msg.setWindowTitle("Unsaved Data")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Save | QMessageBox.Cancel)
#             msg.buttonClicked.connect(self.msgbtn)

            ret = msg.exec()
#             print(ret)
            if ret == 1024: # Ok
                self.myclose()
                return True
            elif ret == 2048: # Save
                self.save()
                return False
            elif ret == 4194304: # Cancel
                return False
        else:
             # ask the user if they want to save
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Are you sure you want to exit?")
            msg.setWindowTitle("Exit warning")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
#             msg.buttonClicked.connect(self.msgbtn)

            ret = msg.exec()
#             print(ret)
            if ret == 1024: # Ok
                self.myclose()
                return True
            elif ret == 4194304: # Cancel
                return False
            
    # actually close
    def myclose(self): #############################################################################################
        self.abort()
        # end any loops that might be running
    # Data loop
        try:
            self.data_end_now = True
            self.data_loop.join() 
        except: pass
    # Graph loop
        try:
            self.graph_end_now = True
            self.graph_loop.join() 
        except: pass
    # auto-save loop
        try:
            self.auto_save_on = False
            self.auto_save_loop.join() 
        except: pass
    # moving loop
        try:
            self.motor_stop_now = True
            self.move_loop.join() 
        except: pass
    # running loop
        try:
            self.abort_now = True
            self.run_loop.join() 
        except: pass
    # close resource manager
        try: 
            self.popup.rm.close()
        except: pass   
    # Close popups
        try:
            self.cw.mpc_popup.close()
        except: pass
        try:
            self.cw.param_popup.close()
        except: pass
        
        print(self.data)
#         try:
#             for pic in self.pics:
#                 display(pic)
#         except: pass
        self.window.myclose()
        try: self.window.myclose()
        except: pass
        self.CCD.clear_cam()
        
        
#####################################################################################################################################
##********************** Miscellaneous ********************************************************************************************##
#####################################################################################################################################

#     def move_stage_dist(self):
#         self.t.move(dist=to_num(self.cw.move_dist_input.text()))
#         self.cw.move_dist_input.setText("")
        
#     def move_stage_loc(self):
#         self.t.go_to(position=to_num(self.cw.move_loc_input.text()))
#         self.cw.move_loc_input.setText("")
            
    def display_command(self, text, t = current_time(), show=False): #########################################################
        t = current_time()
        message = t + ": " + text
        if show:
            self.ow.most_recent_command.append(message)
            self.ow.most_recent_command.moveCursor(QTextCursor.End)
        print(message)
        
    def display_action(self, text, t = current_time(), show=False): #########################################################
        self.display_command(text, t, show)
        #         t = current_time()
#         message = t + ": " + text
#         if show:
#             self.ow.most_recent_action.append(message)
#             self.ow.most_recent_action.moveCursor(QTextCursor.End)
#         print(message)
        
        
#             self.ow.most_recent_command.setText(text)
#             self.ow.recent_command_time.setText("executed at " + current_time())
#         except:
#             print("Couldn't display command", text, "at",current_time())
#         if success:
#             self.most_recent_command.setText(text + " (success)")
#         else:
#             self.most_recent_command.setText(text + " (failure)")

    def reset(self): #############################################################################################
        try:
            self.abort()
            self.abort_now = True
            self.run_loop.join() 
        except:
            pass
        try:
            self.run_number = int(max(self.data['run']))+1
        except:
            self.run_number = 1
#         print("Run number = ",self.run_number)
        self.display_action("Run number set to " + str(self.run_number),show=True)
#         self.pw.progress.setValue(0)
#         self.t.zero()
        