class Pump_Action():
    def __init__(self, volume, v_units, rate, r_units, in_pump, out_pump="None"):
        self.volume = volume
        self.v_units = v_units
        self.rate = rate
        self.r_units = r_units
        self.in_pump = in_pump
        self.out_pump = out_pump
        
        self.vukey = {"ML":"mL",
                      "UL":"uL"}
        
        self.rukey = {"MM":"mL/min",
                      "MH":"mL/hr",
                      "UH":"uL/hr"}
        
    def print_command(self):
        if self.out_pump=="None":
            return "Infuse {} {} from {} at {} {}".format(self.volume, 
                                                           self.vukey[self.v_units], 
                                                           self.in_pump, 
                                                           self.rate, 
                                                           self.rukey[self.r_units])
        else:
            return "Infuse {} {} from {} at {} {}, withdraw from {}".format(self.volume, 
                                                           self.vukey[self.v_units], 
                                                           self.in_pump, 
                                                           self.rate, 
                                                           self.rukey[self.r_units],
                                                           self.out_pump)
        
class Collect_Action():
    def __init__(self, tint, ttot, tmult=1):
        self.tint = tint # collection time interval
        self.ttot = ttot # total collection time
        self.tmult = tmult # time multiplier
        
    def print_command(self):
        if self.tmult != 1:
            return "Collect every {} (*{}^n) s for {} s".format(self.tint,
                                                             self.tmult,
                                                             self.ttot)
        return "Collect every {} s for {} s".format(self.tint,
                                                    self.ttot)

        