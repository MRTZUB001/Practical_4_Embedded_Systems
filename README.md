# Practical_4_Embedded_Systems
Using GIT to contribute code to prac4

#!/usr/bin/python

#Import modules
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import datetime
import os

#Set GPIO pin numbering to BCM
GPIO.setmode(GPIO.BCM)

#ADC Pinout Config
#IC Pin definition
#Configures the chip to use the software SPI configuration
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

#Switch pin number setup
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
