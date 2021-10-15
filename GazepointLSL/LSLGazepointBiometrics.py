######################################################################################
# LSLGazepoint.py - LSL interface
# Written in 2019 by Gazepoint www.gazept.com
#
# To the extent possible under law, the author(s) have dedicated all copyright 
# and related and neighboring rights to this software to the public domain worldwide. 
# This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along with this 
# software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
######################################################################################

# This Python script uses the Open Gaze API to communicate with the Gazepoint Control 
# application. Eye gaze data is read via the Open Gaze API, and then streamed to LSL.

import socket
import time
import re

import pylsl as lsl

# Commands to send to the Open Gaze API
requests = ['<SET ID="ENABLE_SEND_TIME" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_POG_FIX" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_DIAL" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_GSR" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_HR" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_HR_PULSE" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_DATA" STATE="1"/>\r\n']

requests = ['<SET ID="ENABLE_SEND_TIME" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_POG_FIX" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_DATA" STATE="1"/>\r\n']


# Socket send
def send(sock,msg):
    msgb = msg.encode()
    print('Sending:', msgb,'\n')
    totalsent = 0
    while totalsent < len(msgb):
        sent = sock.send(msgb[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
   
# Socket receive   
def receive(sock):
    msg = ''
    numbytes = 0
    t0 = time.time()
    while True:
        chunk = sock.recv(1)
      
        if (len(chunk) == 0):
            break
        msg = msg + (chunk.decode())
        if (msg.endswith('\r\n')):
            break
    
    return msg

if __name__ == "__main__":
    # Connect to Gazepoint Control
    s = socket.socket()
    s.connect(('127.0.0.1',4242))
    
    print('Connected')
    
    # Send request to start streaming data
    numreq = len(requests)
    indreq = 0
    for i in range(numreq):
        send(s,requests[i])
        msg = receive(s)
    
    # Determine serial number
    sn = "000000000"  
    send(s,'<GET ID="SERIAL_ID" />\r\n')
    msg = receive(s)
    m = re.search('(?<=<ACK ID="SERIAL_ID" VALUE=")\d*\.\d+|\d+(?=" />)',msg)
    if (m != None):
        sn = m.group(0)    
    print("Gazepoint device SN: ",'gazepoint'+sn)
    # Initialize LSL entry
    info_gaze = lsl.StreamInfo('GazepointEyeTracker','gaze',6,60,'float32','gazepoint'+sn)
    info_bio = lsl.StreamInfo('GazepointBiometrics','bio',7,60,'float32','gazepointbio')
    
    # Set meta-data for LSL entry
    info_gaze.desc().append_child_value("manufacturer","Gazepoint")
    channels = info_gaze.desc().append_child("channels")
    channels.append_child("channel").append_child_value("label","FPOGX") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","FPOGY") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","FPOGS") \
                                    .append_child_value("unit","seconds") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","FPOGD") \
                                    .append_child_value("unit","seconds") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","FPOGID") \
                                    .append_child_value("unit","integer") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","FPOGV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","gaze") 
                 
    info_bio.desc().append_child_value("manufacturer","Gazepoint")
    channels_bio = info_bio.desc().append_child("channels")                 
    channels_bio.append_child("channel").append_child_value("label","DIAL") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","bio")    
    channels_bio.append_child("channel").append_child_value("label","DIALV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","bio")   
    channels_bio.append_child("channel").append_child_value("label","GSR") \
                                    .append_child_value("unit","ohms") \
                                    .append_child_value("type","bio") 
    channels_bio.append_child("channel").append_child_value("label","GSRV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","bio")    
    channels_bio.append_child("channel").append_child_value("label","HR") \
                                    .append_child_value("unit","bpm") \
                                    .append_child_value("type","bio")  
    channels_bio.append_child("channel").append_child_value("label","HRV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","bio")                                          
    channels_bio.append_child("channel").append_child_value("label","HRP") \
                                    .append_child_value("unit","integer") \
                                    .append_child_value("type","bio")   
    
    # Make an LSL outlet
    outlet_gaze = lsl.StreamOutlet(info_gaze)
    outlet_bio = lsl.StreamOutlet(info_bio)
    
    # Continuously stream data and push each data sample to the LSL
    while True:
        # Reset data values to 0
        rec_time = 0
        rec_fpogx = 0
        rec_fpogy = 0
        rec_fpogs = 0
        rec_fpogd = 0
        rec_fpogid = 0
        rec_fpogv = 0
        rec_dial = 0
        rec_dialv = 0
        rec_gsr = 0
        rec_gsrv = 0
        rec_hr = 0
        rec_hrv = 0
        rec_hrp = 0
        
        # Read data
        msg = receive(s)
        
        # Data looks like: '<REC TIME="199.98715" FPOGX="0.26676" FPOGY="0.99285" FPOGS="199.84114" FPOGD="0.14601" FPOGID="352" FPOGV="1" DIAL="30" DIALV="1" GSR="67296" GSRV="1" HR="53" HRV="1" HRP="50"/>\r\n'
        
        # Parse data string to extract values
        m = re.search('(?<=TIME=")\d*\.\d+|\d+(?=" FPOGX)',msg)
        if (m != None):
            rec_time = float(m.group(0))

        m = re.search('(?<=FPOGX=")\d*\.\d+|\d+(?=" FPOGY)',msg)
        if (m != None):
            rec_fpogx = float(m.group(0))
            
        m = re.search('(?<=FPOGY=")\d*\.\d+|\d+(?=" FPOGS)',msg)
        if (m != None):
            rec_fpogy = float(m.group(0))
            
        m = re.search('(?<=FPOGS=")\d*\.\d+|\d+(?=" FPOGD)',msg)
        if (m != None):
            rec_fpogs = float(m.group(0))
            
        m = re.search('(?<=FPOGD=")\d*\.\d+|\d+(?=" FPOGID)',msg)
        if (m != None):
            rec_fpogd = float(m.group(0))
            
        m = re.search('(?<=FPOGID=")\d*\.\d+|\d+(?=" FPOGV)',msg)
        if (m != None):
            rec_fpogid = float(m.group(0))
            
        m = re.search('(?<=FPOGV=")\d*\.\d+|\d+(?=" DIAL)',msg)
        if (m != None):
            rec_fpogv = float(m.group(0))            
        
        m = re.search('(?<=DIAL=")\d*\.\d+|\d+(?=" DIALV)',msg)
        if (m != None):
            rec_dial = float(m.group(0)) 
            
        m = re.search('(?<=DIALV=")\d*\.\d+|\d+(?=" GSR)',msg)
        if (m != None):
            rec_dialv = float(m.group(0))  
            
        m = re.search('(?<=GSR=")\d*\.\d+|\d+(?=" GSRV)',msg)
        if (m != None):
            rec_gsr = float(m.group(0))  
            
        m = re.search('(?<=GSRV=")\d*\.\d+|\d+(?=" HR)',msg)
        if (m != None):
            rec_gsrv = float(m.group(0))  
            
        m = re.search('(?<=HR=")\d*\.\d+|\d+(?=" HRV)',msg)
        if (m != None):
            rec_hr = float(m.group(0))             

        m = re.search('(?<=HRV=")\d*\.\d+|\d+(?=" HRP)',msg)
        if (m != None):
            rec_hrv = float(m.group(0))                  
            
        m = re.search('(?<=HRP=")\d*\.\d+|\d+(?=" />)',msg)
        if (m != None):
            rec_hrp = float(m.group(0))     
            
        
        # Push data to LSL
        samplegaze = [rec_fpogx, rec_fpogy, rec_fpogs, rec_fpogd, rec_fpogid, rec_fpogv]
        samplebio = [rec_dial, rec_dialv, rec_gsr, rec_gsrv, rec_hr, rec_hrv, rec_hrp]
        outlet_gaze.push_sample(samplegaze)
        outlet_bio.push_sample(samplebio)
        
        
    s.close()
    
    