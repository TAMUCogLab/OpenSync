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

def OpenSync_path():

    return str(os.path.dirname(OpenSync.__file__))
def record_data(save_path):


    LabRecorder_path = OpenSync_path() + "\\LabRecorder\\LabRecorderCLI.exe"
    
    XDF_save_command = LabRecorder_path + " " + save_path + " " + "'searchstr'"
    subprocess.Popen(XDF_save_command, shell=True)