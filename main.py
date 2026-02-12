import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.high_level_commander import HighLevelCommander

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

URI = "radio://0/80/2M/E7E7E7E701"

DEFAULT_HEIGHT = 0.5


def log_stab_callback(timestamp, data, logconf):
    print(
        f"[{timestamp}] "
        f"Roll={data['stabilizer.roll']:.3f}, "
        f"Pitch={data['stabilizer.pitch']:.3f}, "
        f"Yaw={data['stabilizer.yaw']:.3f}"
    )

def take_off_simple(scf):
    hlc = HighLevelCommander(scf.cf)
    hlc.takeoff(DEFAULT_HEIGHT, 2.0)
    time.sleep(2.5)
    hlc.land(0.0, 2.0)
    time.sleep(2.5)
    hlc.stop()

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
        if state["hlc"] is None:
            state["hlc"] = HighLevelCommander(scf.cf)
            state["hlc"].takeoff(DEFAULT_HEIGHT, 2.0)
            time.sleep(2.5)
            state["pos"] = {"x": 0.0, "y": 0.0, "z": DEFAULT_HEIGHT, "yaw": 0.0}
        return True

    if state["hlc"] is None:
        print("must do s first")
        return True

    hlc = state["hlc"]
    pos = state["pos"]

    #q3
    if c == 'u':
        pos["z"] += float(parts[1])
        hlc.go_to(pos["x"], pos["y"], pos["z"], pos["yaw"], 1.0)
        time.sleep(1.5)
        return True

    #q4
    if c == 'd':
        pos["z"] -= float(parts[1])
        hlc.go_to(pos["x"], pos["y"], pos["z"], pos["yaw"], 1.0)
        time.sleep(1.5)
        return True
    #q5
    if c == 'f':
        pos["x"] += float(parts[1])
        hlc.go_to(pos["x"], pos["y"], pos["z"], pos["yaw"], 1.0)
        time.sleep(1.5)
        return True
    #q6
    if c == 'b':
        pos["x"] -= float(parts[1])
        hlc.go_to(pos["x"], pos["y"], pos["z"], pos["yaw"], 1.0)
        time.sleep(1.5)
        return True
    #q7
    if c == 'l':
        pos["yaw"] += float(parts[1])
        hlc.go_to(pos["x"], pos["y"], pos["z"], pos["yaw"], 1.0)
        time.sleep(1.5)
        return True
    #q8
    if c == 'r':
        pos["yaw"] -= float(parts[1])
        hlc.go_to(pos["x"], pos["y"], pos["z"], pos["yaw"], 1.0)
        time.sleep(1.5)
        return True
    #q9
    if c == 'n':
        hlc.land(0.0, 2.0)
        time.sleep(2.5)
        hlc.stop()
        state["hlc"] = None
        state["pos"] = None
        return True

    return True


if __name__ == "__main__":
    cflib.crtp.init_drivers()

    lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch', 'float')
    lg_stab.add_variable('stabilizer.yaw', 'float')

    state = {"hlc": None, "pos": None}


    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        while True:
            cmd = input("> ")
            cont = handle_commands(cmd, scf, lg_stab, state)
            if cont is False:
                break

