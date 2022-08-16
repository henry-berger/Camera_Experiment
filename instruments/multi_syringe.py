import numpy as np
from .syringe import Syringe
import sys
sys.path.append('../')
import utils

class All_Pumps:
    def __init__(self, pumps=None,port="None",parent=None,diameters=[5,5,5]):
        self.status = -1
        self.states = {-1: "None",0: "buffer (pump #1)", 1: "DDM:buffer (pump #2)", 2: "target:DDM:buffer (pump #3)"}
        self.p = parent

        if not pumps==None:
            self.ps = pumps # pump 0, pump 1, pump 2
        elif not port==None:
            self.ps = [
                Syringe(diameters[0],port_name=port, pump_num=0),
                Syringe(diameters[1],port_name=port, pump_num=1),
                Syringe(diameters[2],port_name=port, pump_num=2)
            ]
        self.last_event = -1    
        
    def exchange(self, inf, wdr, volume=np.nan, rate=np.nan, 
             v_units="ML", r_units="MM"):
        if np.isnan(volume):
            volume = self.p.pump_vol
        if np.isnan(rate):
            rate = self.p.pump_rate
        self.p.last_pump_event = self.p.CCD.time()

    # direction
        self.ps[inf].r_w("DIR INF *", 
                    wdr, "DIR WDR")
    # rate
        self.ps[inf].r_w("RAT", rate, r_units, "*", 
                    wdr, "RAT", rate, r_units)
#         self.ps[inf].r_w("RAT", r_units, "*", 
#                     wdr, "RAT", r_units)
    # volume
        self.ps[inf].r_w("VOL", volume, "*", 
                    wdr, "VOL", volume)
        self.ps[inf].r_w("VOL", v_units, "*", 
                    wdr, "VOL", v_units)
    # run
        self.ps[inf].r_w("RUN", "*", 
                    wdr, "RUN")
        self.status = inf
        self.update_status_display()
        
    def pump(self, p, volume=np.nan, rate=np.nan, 
             v_units="ML", r_units="MM"):
        if np.isnan(volume):
            volume = self.p.pump_vol
        if np.isnan(rate):
            rate = self.p.pump_rate
        
            
        self.p.last_pump_event = self.p.CCD.time()
        self.ps[p].go(volume,rate, v_units, r_units)
        self.status = p
        self.update_status_display()

    def update_status_display(self):
        try:
            self.p.ow.liquid_display.setText(str(self.get_status()))
        except:
            print("Couldn't change status")
            
    def stop_all(self):
        for p in self.ps:
            try:
                p.stop()
            except:
                try: p.stop()
                except: pass
            
    def pause_all(self):
        for p in self.ps:
            try:
                p.pause()
            except:
                pass
        
    def get_status(self):
        return self.states[self.status]

    def time_since_last_event(self):
        if self.last_event==-1:
            return -1
        else:
            return utils.gt()-self.last_event