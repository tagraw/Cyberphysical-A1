import logging
import time

from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.high_level_commander import HighLevelCommander
import cflib.crtp

logging.basicConfig(level=logging.ERROR)

URI = "radio://0/80/2M/E7E7E7E701"  

def main():
    cflib.crtp.init_drivers()

    cf = Crazyflie(rw_cache="./cache")

    with SyncCrazyflie(URI, cf=cf) as scf:
        hlc = HighLevelCommander(scf.cf)

        time.sleep(1.0)

        print("Taking off...")
        hlc.takeoff(0.5, 2.0)  
        time.sleep(2.5)

        print("Hovering...")
        time.sleep(2.0)

        print("Landing...")
        hlc.land(0.0, 2.0)
        time.sleep(2.5)

        hlc.stop()
        print("Done.")

if __name__ == "__main__":
    main()
