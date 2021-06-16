THRESHOLD = (120, 165)
BINARY_VISIBLE = True 

import sensor, image, time, pyb, math

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)
count = 0

while(True):
    clock.tick()
    img = sensor.snapshot().binary([THRESHOLD]) if BINARY_VISIBLE else sensor.snapshot()

    line = img.get_regression([(255, 255) if BINARY_VISIBLE else THRESHOLD], False, (0, 0 , 160, 25))

    if (line):
        count = 0
        img.draw_line(line.line(), color = 127)
        print("line.theta() =  %f " % (line.theta()))
        print("line.rho() =  %f " % (line.rho()))
        if (line.rho() < 0) :
            off_axis = - abs(line.rho()) / math.cos(math.radians(line.theta())) - 80
        else :
            off_axis = abs(line.rho()) / math.cos(math.radians(line.theta())) - 80
        print (" off-axis = %f" % (off_axis))

        if (abs(off_axis) < 30) :
            print("go straight1")
            uart.write(("/goStraight/run 60 \r\n").encode())
        elif (off_axis > 30) :
            if (line.theta() > 50 and line.theta() < 90) :
                print("go straight2")
                uart.write(("/goStraight/run 60 \r\n").encode())
                time.sleep(1)
                print("turn right2")
                uart.write(("/rotate/run -50 \r\n").encode())
            elif (line.theta() < 130 and line.theta() > 90) :
                print("go straight3")
                uart.write(("/goStraight/run 60 \r\n").encode())
                time.sleep(1)
                print("turn left3")
                uart.write(("/rotate/run 50 \r\n").encode())
            else :
                print("turn left4")
                uart.write(("/rotate/run 50 \r\n").encode())
        elif (off_axis < -30) :
            if (line.theta() > 50 and line.theta() < 90) :
                print("go straight5")
                uart.write(("/goStraight/run 60 \r\n").encode())
                time.sleep(1)
                print("turn right5")
                uart.write(("/rotate/run -50 \r\n").encode())
            elif (line.theta() < 130 and line.theta() > 90) :
                print("go straight6")
                uart.write(("/goStraight/run 60 \r\n").encode())
                time.sleep(1)
                print("turn left6")
                uart.write(("/rotate/run 50 \r\n").encode())
            else :
                print("turn right7")
                uart.write(("/rotate/run -50 \r\n").encode())
    else :
        count += 1
        if (count > 7):
            print("/stop/run \r\n")
            uart.write(("/stop/run \r\n").encode())

    print("FPS %f, mag = %s" % (clock.fps(), str(line.magnitude()) if (line) else "N/A"))

