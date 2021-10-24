from .sensors import EEG
from .sensors import EyeTracking
from .sensors import BodyMotion
from .markers import marker
from .i_o import Keyboard
from .i_o import Mouse
from .i_o import Gamepad
from .i_o import Joystick

import subprocess
import os
import OpenSync
import time

def OpenSync_path():

    return str(os.path.dirname(OpenSync.__file__))
def record_data(save_path):


    LabRecorder_path = OpenSync_path() + "\\LabRecorder\\LabRecorderCLI.exe"
    
    XDF_save_command = LabRecorder_path + " " + save_path + " " + "'searchstr'"
    time.sleep(3)
    subprocess.Popen(XDF_save_command, shell=True)

def stop_record():
    try:
        subprocess.Popen("TASKKILL /F /IM LabRecorderCLI.exe", shell=True)
    except ValueError:
        print("No LabRecorderCLI Task is Open!")
    try:
        subprocess.Popen("TASKKILL /F /IM Gazepoint.exe", shell=True)
    except ValueError:
        print("No Gazepoint Task is Open!")
    try:
        subprocess.Popen("TASKKILL /F /IM BodyBasicsLSL.exe", shell=True)
    except ValueError:
        print("No Kinect Task is Open!")
        
