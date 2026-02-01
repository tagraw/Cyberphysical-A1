import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.log import LogConfig
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# TODO URI to the Crazyflie — change after we get a drone
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')


def main():
    print("Commands: i, s, u x, d x, f x, b x, l x, r x, n")

    cflib.crtp.init_drivers()

    # Create Crazyflie object
    cf = Crazyflie(rw_cache='./cache')
    
    lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch', 'float')
    lg_stab.add_variable('stabilizer.yaw', 'float')

    with SyncCrazyflie(URI, cf=cf) as scf:


if __name__ == "__main__":
    main()
