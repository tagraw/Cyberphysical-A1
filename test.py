Conversation opened. 1 unread message.

Skip to content
Using UTmail Mail with screen readers
Enable desktop notifications for UTmail Mail.
   OK  No thanks

1 of 3,205
Test Script
Inbox

Shashank Iswara
Attachments
4:53 PM (40 minutes ago)
to me


 One attachment
  •  Scanned by Gmail

To


---------- Forwarded message ---------
From: Shashank Iswara <shashankiswara@utexas.edu>
Date: Wed, Feb 11, 2026 at 4:53 PM
Subject: Test Script
To: <tanviagrawal@utexas.edu>





--
Tanvi Agrawal | Computer Science
The University of Texas at Austin  
tanviagrawal@utexas.edu | LinkedIn
test.py (1K)
import time
import logging

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
test.py
Displaying test.py. 
