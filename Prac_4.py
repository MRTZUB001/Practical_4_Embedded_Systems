# global variables
values = [0]*8
t = 0.5 # sample time interval
timer = 0 # total time elapsed
names = ['Time','Timer','Pot','Temp','Light']
stopFlag = True
monitor = ['']*5
displayList = monitor*5
n=0

# function definition: threaded callback
def callback1(channel): # reset
        global timer, monitor, names
        os.system('cls' if os.name == 'nt' else 'clear') # clear console
        timer =0 # reset timer
        monitor[1] = time.strftime("%H:%M:%S",time.gmtime(0))
        print ('{0:>8} | {1:>8} | {2:>5} | {3:>5} | {4:>4}'.format(*names))
        print('{0:>8} | {1:>8} | {2:>4}V | {3:>4}C | {4:>3}%'.format(*monitor))

def callback2(channel): # freq
        global t
        if t == 0.5:
                t = 1
        elif t == 1:
                t = 2
        elif t == 2:
                t = 0.5

def callback3(channel): # stop
        global stopFlag # false = stop
        global n
        n=0
        if stopFlag == False: stopFlag = True
        elif stopFlag == True: stopFlag = False


def callback4(channel): # display
        global displayList
        for i in range(5):
                print('{0:>8} | {1:>8} | {2:>4}V | {3:>4}C | {4:>3}%'.format(*displayList[i]))

# Under a falling-edge detection, regardless of current execution
# callback function will be called
GPIO.add_event_detect(resetSwitch, GPIO.FALLING, callback=callback1,bouncetime=200)
GPIO.add_event_detect(freqSwitch, GPIO.FALLING, callback=callback2,bouncetime=200)
GPIO.add_event_detect(stopSwitch, GPIO.RISING, callback=callback3,bouncetime=200)
GPIO.add_event_detect(displaySwitch, GPIO.RISING, callback=callback4,bouncetime=200)


print ('{0:>8} | {1:>8} | {2:>5} | {3:>5} | {4:>4}'.format(*names))


while True:
        global t, timer, displayList, values, monitor,n
        try:
                for i in range(8):
                        values[i] = mcp.read_adc(i)
                # delay for a half second
                time.sleep(t)
                timer = timer + t
                monitor[0] = time.strftime("%H:%M:%S",time.gmtime())
                monitor[1] = time.strftime("%H:%M:%S",time.gmtime(timer))
                #monitor[2] = values[0];
                monitor[2] = str(round(values[0]*3.3/1023,1))
                monitor[3] = str(round(100*((values[4]*3.3/1023)-0.5),1)) # @ 25C, Vout = 0.5V
                monitor[4] = str(round(values[2]*100/1023))
                if stopFlag:
                        print('{0:>8} | {1:>8} | {2:>4}V | {3:>3}C | {4:>3}%'.format(*monitor))
                else:
                        if n<5:
                                displayList[n] = [monitor[0],monitor[1],monitor[2],monitor[3],monitor[4]]
                                n+=1
        except KeyboardInterrupt:
                GPIO.cleanup() # clean up GPIO on CTRL+C exit

GPIO.cleanup() # clean up GPIO on normal exit

