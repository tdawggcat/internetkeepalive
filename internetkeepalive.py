#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

InternetPowerPin = 13
TimeToKeepPowerOff = 1
HostNameToCheck = "script.google.com"
#HostNameToCheck = "asdad9sa0d9as.asdsa90da0sd9sa.com"
NumberOfFailuresFileName = "/home/pi/internetkeepalive/NumberOfAttempts"

# Based on the program running every 15 minutes...
#FailurePowerCycleInterval1 = 4*6
#FailurePowerCycleInterval2 = 4*24*7
FailurePowerCycleInterval1 = 4*6
FailurePowerCycleInterval2 = 4*24*3

PingResponse = os.system("ping -c 1 " + HostNameToCheck)

def PowerCycle():
 GPIO.setup(InternetPowerPin, GPIO.OUT)
 GPIO.output(InternetPowerPin, GPIO.LOW)
 time.sleep(TimeToKeepPowerOff)
 GPIO.output(InternetPowerPin, GPIO.HIGH)
 time.sleep(1)
 GPIO.cleanup()
#end PowerCycle()


if PingResponse == 0:
# print "Success"
 NumberOfFailuresFile = open(NumberOfFailuresFileName,"w")
 NumberOfFailuresFile.write ("0")
 NumberOfFailuresFile.close()
else:
 NumberOfFailuresFile = open(NumberOfFailuresFileName,"r")
 NumberOfFailures = int(NumberOfFailuresFile.read(10))
 NumberOfFailuresFile.close()
 NumberOfFailures = NumberOfFailures + 1
 NumberOfFailuresFile = open(NumberOfFailuresFileName,"w")
 NumberOfFailuresFile.write (str(NumberOfFailures))
 NumberOfFailuresFile.close()
# print "Failed",NumberOfFailures," times"

 if (NumberOfFailures < FailurePowerCycleInterval1):
 #Failed less than the 1st threshold
  PowerCycle()
 else:
  if (NumberOfFailures < FailurePowerCycleInterval2):
   #Failed more than or equal to the 1st threshold, and less than the 2nd threshold
   if (NumberOfFailures % FailurePowerCycleInterval1 == 0):
    #Every multiple of 1st threshold up to the 2nd threshold
    PowerCycle()
  else:
   #Failed more than the 2nd threshold
   if (NumberOfFailures % FailurePowerCycleInterval2 == 0):
    #Every multiple of 2nd threshold
    PowerCycle()


