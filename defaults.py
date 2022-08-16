def get_default_parameters():
    params = {
        'volume'            : 0.1,    #           volume dispensed each time 
        
        'v_units'           : 'ML',   #          ML: mL
                                      #          UL: uL
        
        'rate'              : 1,      #          pump rate for syringe pumps
        
        'r_units'           : 'MM',   #          MM: mL/min
                                      #          MH: mL/hr
                                      #          UH: uL/hr
        
        'target time int'   : 0.2,    # (s)      Time between initial measurements 
                                      #             when target:DDM:buffer is injected (s)
        
        'target total time' : 2,      # (s)      Total observation time for target:DDM:buffer
        
        'target time mult'  : 1.25,   # (N/A)    Ratio between successive measurement intervals
                                      #             when target:DDM:buffer is injected (s)
        
        'other time int'    : 0.3,    # (s)      Time between initial measurements 
                                      #             when buffer or DDM:buffer is injected (s)
        
        'other total time'  : 2,      # (s)      Total observation time for buffer and DDM:buffer
        
        'other time mult'   : 1,      # (N/A)    Ratio between successive measurement intervals
                                      #             when buffer or DDM:buffer is injected (s)
        }
    return  params