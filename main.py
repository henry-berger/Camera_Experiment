import utils
from GUI import GUI
import configargparse


p = configargparse.ArgumentParser()
p.add_argument('--volume',              type=float,     default=0.1,    help="volume dispensed each time") 
p.add_argument('--v_units',             type=str,       default='ML',   
                                        choices=["ML","UL"],            help="Volume units")
p.add_argument('--rate',                type=float,     default=1.0,    help="pump rate for syringe pumps")
p.add_argument('--r_units',             type=str,       default='MM',   
                                        choices=["MM","MH","UH"],       help="units for rate (mL/min, mL/hr, uL/hr")
p.add_argument('--target_time_int',     type=float,     default=0.2,    help="Time between initial measurements when target:DDM:buffer is injected (s)")
p.add_argument('--target_total_time',   type=float,     default=2.0,    help="Total observation time for target:DDM:buffer (s)")
p.add_argument('--target_time_mult',    type=float,     default=1.25,   help="Ratio between successive measurement intervals when target:DDM:buffer is injected (s)")
p.add_argument('--other_time_int',      type=float,     default=0.3,    help="Time between initial measurements when buffer or DDM:buffer is injected (s)")
p.add_argument('--other_total_time',    type=float,     default=2.0,    help="Total observation time for buffer and DDM:buffer (s)")
p.add_argument('--other_time_mult',     type=float,     default=1.0,    help="Ratio between successive measurement intervals")


if __name__ == "__main__":
    params = p.parse_args()

    app = utils.start_QApplication()
    p = GUI(params=params)
    p.show()
    app.exec()