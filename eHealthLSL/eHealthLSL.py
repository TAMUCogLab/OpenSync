#### IMPORTANT: YOU NEED TO DEPLOY THE GSR_SerialSend.ino SCRIPT ON THE ARDUINO ####

import serial
from pylsl import StreamInfo, StreamOutlet
import sys

ser = serial.Serial(sys.argv[1], 115200)


info = StreamInfo(name='eHealthGSR', type='Voltage', channel_count=3, channel_format='float32', source_id='eHealthGSR_id')

outlet = StreamOutlet(info)

while True:

    C=-1000
    R=-1000
    V=-1000
    ser_bytes = (ser.readline()).decode("utf-8")

    if ser_bytes[0] == "C":
        C = float(ser_bytes[1:-2])
        print(C)
    elif ser_bytes[0] == "R":
        R = float(ser_bytes[1:-2])
        print(R)
    elif ser_bytes[0] == "V":
        V = float(ser_bytes[1:-2])
        print(V)
    outlet.push_chunk([C,R,V])
