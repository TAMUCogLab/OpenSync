from pyOpenBCI import OpenBCICyton
from pylsl import StreamInfo, StreamOutlet
from pathlib import Path
import os
import subprocess
import numpy as np
from mindwavelsl import MindwaveLSL
import OpenSync

class EEG:
    def __init__(self):
        pass

    def OpenBCI_Cyton(self,port="COM3", daisy=False):

        if daisy:
            subprocess.Popen(['python.exe', OpenSync.OpenSync_path() + "\\OpenBCILSL\\OpenBCILSL_Daisy.py", port])
        else:
            subprocess.Popen(['python.exe', OpenSync.OpenSync_path() + "\\OpenBCILSL\\OpenBCILSL.py", port])

    def Unicorn(self):
        subprocess.Popen(OpenSync.OpenSync_path() + "\\UnicornLSL\\UnicornLSL.exe", shell=True)

    def LiveAmp(self, n_channels, sfreq):
        subprocess.Popen([OpenSync.OpenSync_path() + "\\LiveAmpLSL\\LiveAmp-LSL.exe", str(n_channels), str(sfreq)], shell=True)

    def Muse(self):
        subprocess.check_output("start bluemuse://setting?key=primary_timestamp_format!value=LSL_LOCAL_CLOCK_NATIVE", shell=True)
        subprocess.check_output("start bluemuse://start?streamfirst=true", shell=True)

    def Mindwave(self):
        mwlsl = MindwaveLSL('localhost', 13854)
        mwlsl.setup()
        mwlsl.run()

class BodyMotion:
    def __init__(self):
        pass
    def KinectBodyBasics(self):
        subprocess.Popen(OpenSync.OpenSync_path() + "\\KinectBodyBasicsLSL\\BodyBasicsLSL.exe", shell=True)

class EyeTracking:
    def __init__(self):
        pass
    def Gazepoint(self, biometrics=False):
        os.system("TASKKILL /F /IM Gazepoint.exe")
        subprocess.Popen("C:/Program Files (x86)/Gazepoint/Gazepoint/bin64/Gazepoint.exe", shell=True)
        if biometrics:
            subprocess.Popen(['python.exe',OpenSync.OpenSync_path() + "\\GazepointLSL\\LSLGazepointBiometrics.py"])
        else:
            subprocess.Popen(['python.exe',OpenSync.OpenSync_path() + "\\GazepointLSL\\LSLGazepoint.py"])
            
class GSR:
    def __init__(self):
        pass
    def eHealth(self, port = "COM3"):
        subprocess.Popen(['python.exe',OpenSync.OpenSync_path() + "\\eHealthLSL\\eHealthLSL.py", port])
