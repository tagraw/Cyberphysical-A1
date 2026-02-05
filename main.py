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

DEFAULT_HEIGHT = 0.5


def log_stab_callback(timestamp, data, logconf):
    print(
        f"[{timestamp}] "
        f"Roll={data['stabilizer.roll']:.3f}, "
        f"Pitch={data['stabilizer.pitch']:.3f}, "
        f"Yaw={data['stabilizer.yaw']:.3f}"
    )

def take_off_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(4)

def handle_commands(cmd, scf, lg_stab, state):
    parts = cmd.strip().split()
    if not parts:
        return True

    c = parts[0]

    # q1
    if c == 'i':
        scf.cf.log.add_config(lg_stab)
        lg_stab.data_received_cb.add_callback(log_stab_callback)
        lg_stab.start()
        time.sleep(2)
        lg_stab.stop()
        return True

    #q2
    if c == 's':
        if state["mc"] is None:
            state["mc"] = MotionCommander(scf, default_height=DEFAULT_HEIGHT)
        return True

    if state["mc"] is None:
        print("must do s first")
        return True 
        
    mc = state["mc"]


    #q3
    if c == 'u':
        mc.up(float(parts[1]))
        return True

    #q4
    if c == 'd':
        mc.down(float(parts[1]))
        return True
    #q5
    if c == 'f':
        mc.forward(float(parts[1]))
        return True
    #q6
    if c == 'b':
        mc.back(float(parts[1]))
        return True
    #q7
    if c == 'l':
        mc.turn_left(float(parts[1]))
        return True
    #q8
    if c == 'r':
        mc.turn_right(float(parts[1]))
        return True
    #q9
    if c == 'n':
        mc.land()
        mc.stop()
        state["mc"] = None
        return True

    return True


if __name__ == "__main__":
    cflib.crtp.init_drivers()

    lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch', 'float')
    lg_stab.add_variable('stabilizer.yaw', 'float')

    state = {"mc": None}


    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        while True:
            cmd = input("> ")
            cont = handle_commands(cmd, scf, lg_stab, state)
            if cont is False:
                break

