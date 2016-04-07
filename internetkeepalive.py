#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

InternetPowerPin = 13
TimeToKeepPowerOff = 10
HostNameToCheck = "script.google.com"
#HostNameToCheck = "asdad9sa0d9as.asdsa90da0sd9sa.com"
NumberOfFailuresFileName = "/home/pi/internetkeepalive/NumberOfAttempts"

PingResponse = os.system("ping -c 1 " + HostNameToCheck)
if PingResponse == 0:
 print "Success"
 NumberOfFailuresFile = open(NumberOfFailuresFileName,"w")
 NumberOfFailuresFile.write ("0")
 NumberOfFailuresFile.close()
else:
 NumberOfFailuresFile = open(NumberOfFailuresFileName,"r")
 NumberOfFailures = int(NumberOfFailuresFile.read(10))
 NumberOfFailuresFile.close()
 NumberOfFailures = NumberOfFailures + 1
 NumberOfFailuresFile = open(NumberOfFailuresFileName,"w")
 NumberOfFailuresString = str(NumberOfFailures)
 NumberOfFailuresFile.write (NumberOfFailuresString)
 NumberOfFailuresFile.close()
 print "Failed",NumberOfFailures," times"

 GPIO.setup(InternetPowerPin, GPIO.OUT)
 GPIO.output(InternetPowerPin, GPIO.LOW)
 time.sleep(TimeToKeepPowerOff)
 GPIO.output(InternetPowerPin, GPIO.HIGH)
 time.sleep(1)
 GPIO.cleanup()

#end else
