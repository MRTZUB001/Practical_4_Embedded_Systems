#!/usr/bin/python

#Import modules
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import datetime
import os

#Set GPIO pin numbering to BCM
GPIO.setmode(GPIO.BCM)

# Configures the chip to use the software SPI configuration
#ADC Pinout Config
#IC Pin definition
SPICLK = 11     # Yellow        (CLK)
SPIMISO = 9     # Brown         (Data_out from slave)
SPIMOSI = 10    # Orange        (Data_in to slave)
SPICS = 8       # Grey          (CS/SHDN)


#Pin connection of chip in circuit
#Vdd & Vref = 3V3
#AGND = 0V
#DGND = 0V
#CH0 -> POT (Connected as 0-3V3)
#CH2 -> LDR (roughly 250ohm with phone flash up to 400Kohm at full dark )
#CH4 -> Temp
resetSwitch = 26
freqSwitch = 19
stopSwitch = 13
displaySwitch = 6
 
#Switch Pin mode setup
#Pull ups
GPIO.setup(resetSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(freqSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#Pull downs
GPIO.setup(stopSwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(displaySwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#IC Pin mode setup
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

#Connects the SPI to the IC chip
mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI,miso=SPIMISO)

# global variable
values = [0]*8                                      # array to read values
t = 0.5                                             # sample time interval
timer = 0                                           # total time elapsed
names = ['Time','Timer','Pot','Temp','Light']       # Headings
monitor = ['']*5                                    # Create array to display

while True:
        global t, timer, values, monitor                                   # use global variables
        try:
                for i in range(8):                                         # read adc pin values
                        values[i] = mcp.read_adc(i)
       
                time.sleep(t)                                              # delay by 't' seconds
                timer = timer + t
                monitor[0] = time.strftime("%H:%M:%S",time.gmtime())       # Time interval
                monitor[1] = time.strftime("%H:%M:%S",time.gmtime(timer))  #Timer
                monitor[2] = str(round(values[0]*3.3/1023,1))              # Convert 10-bit poteniometer reading
             
        except KeyboardInterrupt:
                GPIO.cleanup()                                             # clean up GPIO on CTRL+C exit

GPIO.cleanup()                                                             # clean up GPIO on normal exit
