#!/usr/bin/python

############################################ 
# PROBLEM STATEMENT:
# This program will publish test mqtt messages using the AWS IOT hub
# 
# To test this program you have to run first its companinon aws_iot_sub.py
# that will subscribe and show all the messages sent by this program
#
############################################

############################################
# STEPS:
#
# 1. Sign in to AWS Amazon > Services > AWS IoT > Settings > copy Endpoint
#    This is your awshost
# 
# 2. Change following things in the below program:
#    a. awshost   (from step 1)
#    b. clientId  (Thing_Name)
#    c. thingName (Thing_Name)
#    d. caPath    (root-CA_certificate_Name)
#    e. certPath  (<Thing_Name>.cert.pem)
#    f. keyPath   (<Thing_Name>.private.key)
# 
# 3. Paste aws_iot_pub.py & aws_iot_sub.py python scripts in folder where all unzipped aws files are kept. 
# 4. Provide Executable permition for both the python scripts.
# 5. Run aws_iot_sub.py script
# 6. Run this aws_iot_pub.py python script
#
############################################

# importing libraries
import os
import socket
import ssl
from time import sleep
from random import uniform
import paho.mqtt.client as paho

 
import pyaudio
import wave
import time
from array import array
import pyAesCrypt
import os
form_type=pyaudio.paInt16
channel_no=1
bit_rate=44100
chunk=4096
record_seconds=15
filename='audio1.wav'
#dev_index= 2



connflag = False
 
def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print ("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc) )
 
def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))
 
#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))
 
mqttc = paho.Client()                                        # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
#mqttc.on_log = on_log

#### Change following parameters #### 
awshost = "a1kudj94y1eid7-ats.iot.us-east-1.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "aws_thing1"                                     # Thing_Name
thingName = "aws_thing1"                                    # Thing_Name
caPath = "./ACI_Project/root-CA.crt"                                      # Root_CA_Certificate_Name
certPath = "./ACI_Project/aws_thing1.cert.pem"                            # <Thing_Name>.cert.pem
keyPath = "./ACI_Project/aws_thing1.private.key"                          # <Thing_Name>.private.key
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
 
mqttc.loop_start()                                          # Start the loop

 
#while 1==1
sleep(5)
if connflag == True:
	a=1
	while a == 1 :
 
		audio=pyaudio.PyAudio() #instantiate the pyaudio
		audio.get_default_input_device_info()

		#recording prerequisites
		stream=audio.open(format=form_type,channels=channel_no, 
						rate=bit_rate,
						input=True,
						frames_per_buffer=chunk)

		#starting recording
		frames=[]
		#while True:
		#for i in range(0,int(bit_rate/chunk*record_seconds)):
		data=stream.read(chunk)
		data_chunk=array('h',data)
		vol=max(data_chunk)
		if(vol>=400):
			print("Room is occupied, noise detected")
			frames.append(data)
			#time.sleep(0.5)
		
			mqttc.publish("Sound Detected from RPi-1") # topic: Voice Publishing 
			print("msg sent: Sending From RPi_1 ") # Print sent Voice msg on console
		else:
			mqttc.publish("No Sound Detected from RPi-1") # topic: Voice Publishing 
			print("Available, no noise")
			print("\n") 
			#time.sleep(0.1)

		#end of recording
		stream.stop_stream()
		stream.close()
		audio.terminate()
		#writing to file
		wavfile=wave.open(filename,'wb')
		wavfile.setnchannels(channel_no)
		wavfile.setsampwidth(audio.get_sample_size(form_type))
		wavfile.setframerate(bit_rate)
		wavfile.writeframes(b''.join(frames))#append frames recorded to file
		wavfile.close()
	
		buffersize = 64 * 1024
		password = "decrypt" #Passord to encrypt file
		pyAesCrypt.encryptFile ("audio1.wav", "audio1.wav.aes", password, buffersize) #Encrypt the recorded file
		#pyAesCrypt.decryptFile ("audio1.wav.aes", "audio2.wav", password, buffersize) #To decrypt the encrypted file
		os.remove("audio1.wav") #Delete the file

	
	
else:
	print("waiting for connection...") 
		
  
