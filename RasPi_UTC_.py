import serial
import time
import datetime

ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)

print("Initializing connection....")
time.sleep(3)

ser.reset_input_buffer()

print("HELLO!")
print("connected to: " + ser.portstr)
print("moving")


def get_minute_hand_angle():
    now = datetime.datetime.now()
    minute = now.minute
    return (minute / 60.0) * 360.0

# 1 - 6
# 15 - 90
# 30 - 180
# 60 - 360

def get_second_hand_angle():
    now = datetime.datetime.now()
    second = now.second
    return (second / 60.0) * 360.0

def get_hour_hand_angle():
    now = datetime.datetime.now()
    hour = now.hour
    return (hour / 24.0) * 360.0

# 1 - 15
# 3 - 45
# 6 - 90
# 12 - 180

while True:
    #ser.write('MOVE 200\n'.encode())
    #time.sleep(5)
    #ser.write(b'MOVE 100\n')
    time.sleep(5)
    
    stepangle = int(get_second_hand_angle()  /360.0 * 800.0)
    ser.write(('UTC_MOVE ' + str(stepangle) + '\n').encode())
    
           
#ser.close()
