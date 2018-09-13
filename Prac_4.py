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
                print('{0:>8} | {1:>8} | {2:>4}V | {3:>4}C | {4:>3}%'.format(*displayList

[i]))

# Under a falling-edge detection, regardless of current execution
# callback function will be called
GPIO.add_event_detect(resetSwitch, GPIO.FALLING, callback=callback1,bouncetime=200)
GPIO.add_event_detect(freqSwitch, GPIO.FALLING, callback=callback2,bouncetime=200)
GPIO.add_event_detect(stopSwitch, GPIO.RISING, callback=callback3,bouncetime=200)
GPIO.add_event_detect(displaySwitch, GPIO.RISING, callback=callback4,bouncetime=200)