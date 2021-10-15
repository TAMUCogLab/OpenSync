import serial
from pylsl import StreamInfo, StreamOutlet

ser = serial.Serial('COM4', 115200)

C=""
R=""
V=""

info = StreamInfo(name='GSR', type='Voltage', channel_count=1, channel_format='string', source_id='GSR_Voltage')

outlet = StreamOutlet(info)

while True:

    ser_bytes = (ser.readline()).decode("utf-8")

    if ser_bytes[0] == "C":
        C = ser_bytes[1:-2]
        #print(C)
    elif ser_bytes[0] == "R":
        R = ser_bytes[1:-2]
        #print(R)
    elif ser_bytes[0] == "V":
        V = ser_bytes[1:-2]
        #print(V)
    outlet.push_sample([V])
