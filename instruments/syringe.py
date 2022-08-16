import pyvisa
import random
import sys
sys.path.append('../')
import utils

class Syringe:
    
#************************ Initialization **************************#

    def __init__(self, diameter, port_name="None", pump_num=0):
        self.pan = pump_num # pump address number
        self.port_name = port_name # address number of the pump
        self.diameter = diameter # diameter (in mm)
        self.connect_to_pump(port_name)
        self.r_w("DIA", diameter) # Sets the diameter successfully
        self.dir = ""
        
    def connect_to_pump(self,port_name):
        if port_name=="None":
            self.inst = Fake_Inst()
        else:
            rm = pyvisa.ResourceManager()
            self.inst = rm.open_resource(port_name)
            self.inst.read_termination = '\x03'  
            self.inst.timeout = 100
            print("Successfully connected to pump(s)")
            
        self.CR = '\x0D' # carriage return
        self.STX = '\x02' # start of packet transmisison indicator
        self.ETX = '\x03' # end of packet transmission indicator

#************************ Read/Write **************************#
        
    """
    Read/Write:
    Write a message to the instrument
    Returns the output
    Will concatenate multiple message parts
    """
    def r_w(self, *message_parts):
    # WRITING
        # concatenate the message
        message = self.strcat1(message_parts)
#         print(message)
        # add the pump number and the carriage return
        full_message = self.strcat(self.pan, message, self.CR)
        print("Wrote", full_message)
        self.inst.write(full_message)
    # READING
        try:
            # get the entire output stream
#             output = self.inst.read()
            output = self.read_careful()
            if '?' in output: 
                print(full_message,'not understood')
                print('Error:', output)
            return output
        except: 
            print("Error: Reading failed")
    
    
#************************ Read/Write **************************#

    """
    Sets direction (checked)
        Infuse: "Infuse"
        Withdraw: "Withdraw"
        Reverse direction: "Reverse"
    """
    def set_direction(self, direction):
        dir_commands = {"Infuse": "INF", "Withdraw":"WDR","Reverse":"REV"}
        return self.r_w("DIR", dir_commands[direction])

    """
    Sets diameter (in millimeters)
    """
    def set_diameter(self, diameter):
        return self.r_w("DIA", diameter) # Sets the diameter successfully

    """
    Sets rate
    Rate: Rate (in units specified)
    Units: 
        UM: uL/min     MM: mL/min
        UH: uL/hr      MH: mL/hr
    """
    def set_rate(self, rate, units="MH"):
        return self.r_w("RAT", rate, units)
    
    """
    UNITS WORK, VOLUME DOESN't
    Sets rate
    Volume: volume (in units specified)
    Units: 
        UL: uL
        ML: mL
    """
    def set_volume(self, volume, units = "ML"):
        if volume < 0 :
            self.set_direction("Withdraw")
            volume *= -1
        else:
            self.set_direction("Infuse")
        self.r_w("VOL", units)
        return self.r_w("VOL", volume)
    
    """
    USUALLY WORKS
    """
    def get_volume(self): 
        self.inst.read_termination = 'L'
        output = self.r_w("DIS")
        print("Output: " + output)
        self.inst.read_termination = '\x03'
        print(self.parse(output))
    
    def example_run(self):
        self.set_rate(1, "MH")
#         self.set_volume(1, "UL")
        self.run()
    
    def pause(self):
        self.r_w('STP')
        
    def stop(self):
        self.r_w('STP')
        try:
            self.r_w('STP')
        except:
            try:
                self.r_w('STP')
            except: pass
        
    def run(self):
        self.r_w('RUN')
        
    def go(self, volume=0, rate=0, v_units="ML", r_units="MH"):
        def f():
#             self.set_volume(volume, v_units)
#             self.set_rate(rate, r_units)
            self.prep(volume, rate, v_units, r_units)
            self.run()
        utils.thread_do(f)
        
    def prep(self, volume=0, rate=0, v_units="ML", r_units="MH"):
        self.set_volume(volume, v_units)
        self.set_rate(rate, r_units)
        
    
        
#************************ Helper Functions **************************#
        
    # concatenates a tuple into one string
    # the input tuple can have any type of variable
    def strcat1(self,parts):
        message = ""
        for part in parts:
            message = message + " " + str(part)
        return(message)

    # concatenates all input variables into one string
    # the inputs can be any type of variable
    def strcat(self,*parts):
        message = ""
        for part in parts:
            message = message + str(part)
        return(message)
    
    def parse(self,message):
        vol = float(message[-6:-1])
        if message[-7] == "W":
            multiplier = -1
        else:
            multiplier = 1
        if message[-1] == "U":
            multiplier /= 1000
        return(round(vol*multiplier, 100))
    
    def read_careful(self):
        message = ""
        while True:
            try:
#                 message = message + str(self.inst.read_bytes(1))
                byte = self.inst.read_bytes(1)
                try:
                    char = byte.decode()
                    o = ord(char)
                    if   o==2: char = "<<"
                    elif o==3: char = ">>"
                    elif o==5: char = " ENQ "
                    elif o==11: char = "   "
                    elif o==7: char = " BEL "
#                     else: print(o,char)
                except:
                    char = "{"+str(byte)+"}"
                message = message + char

#                 message.append(self.inst.read_bytes(1))
            except:
                return message
            
"""
Fake instrument class
Used by the syringe class when there's no syringe connected
"""
class Fake_Inst:
    def __init__(self):
        self.read_termination = 'End'
    def write(self,message):
        print("Wrote "+message)
        
    def read_bytes(self,n):
        r = random.random()
        if r<0.01:
            return 1/0
        elif random.random()%0.1*10<0.5:
            return chr(random.randint(48,58))
        else:
            return chr(random.randint(97,107))
        
    def read(self):
        return "ABCDEF1.000M"