import time
import serial
import sys,tty,termios
class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def get():
    d_1 = input()
    d_2 = input()
    dir = input()
    send = d_1 + " " + d_2 + " " + dir + "\n"
    d_1 = int(d_1)
    d_2 = int(d_2)
    print(send)
    if dir == 'e' :
        print ("start")
        s.write("/goStraight/run -100 \n".encode())
        time.sleep(d_2/8 + 1)
        s.write("/stop/run \n".encode())
        s.write("/turn/run 100 -0.3 \n".encode())
        time.sleep(2.4)
        s.write("/stop/run \n".encode())
        s.write("/goStraight/run -100 \n".encode())
        time.sleep(d_1/8 + 1.5)
        s.write("/stop/run \n".encode())
    if dir == 'w' :
        print ("start")
        s.write("/goStraight/run -100 \n".encode())
        time.sleep(d_2/8 + 1)
        s.write("/stop/run \n".encode())
        s.write("/turn/run 100 0.3 \n".encode())
        time.sleep(2.4)
        s.write("/stop/run \n".encode())
        s.write("/goStraight/run -100 \n".encode())
        time.sleep(d_1/8 + 1.5)
        s.write("/stop/run \n".encode())
    return 1

if len(sys.argv) < 1:
    print ("No port input")
s = serial.Serial(sys.argv[1])
while get():
    i = 0