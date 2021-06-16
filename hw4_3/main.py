import pyb, sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)

def degrees(radians):
    return (180 * radians) / math.pi

uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)
find = False
count = 0
while(True):
    clock.tick()
    img = sensor.snapshot()
    find = False
    for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
        find = True
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        # The conversion is nearly 6.2cm to 1 -> translation
        print_args = (tag.x_translation(), tag.y_translation(), tag.z_translation(), \
            degrees(tag.x_rotation()), degrees(tag.y_rotation()), degrees(tag.z_rotation()))
        # Translation units are unknown. Rotation units are in degrees.
        print("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args)
        #uart.write(("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args).encode())
        off_axis = tag.cx()- 72
        print ("cx = %f, c_y = %f, off_axis = %f" %(tag.cx(), tag.cy(), off_axis))
        if (degrees(tag.y_rotation()) > 10 and degrees(tag.y_rotation()) < 180) :
            count = 0
            if (abs(off_axis) < 15) :
                print ("turn right1")
                uart.write (("/turn/run 50 -0.3 \n").encode())
            elif (off_axis < -50) :
                print ("turn right7")
                uart.write (("/turn/run 50 -0.3 \n").encode())
            elif (off_axis > 70) :
                print ("turn left8")
                uart.write (("/turn/run 70 0.3 \n").encode())
            else :
                print ("go stright3")
                uart.write (("/goStraight/run 70 \n").encode())
        elif (degrees(tag.y_rotation()) < 350 and degrees(tag.y_rotation()) > 180) :
            if (abs(off_axis) < 15) :
                print ("turn left4")
                uart.write (("/turn/run 50 0.3 \n").encode())
            elif (off_axis < -70) :
                print ("turn right7")
                uart.write (("/turn/run 50 -0.3 \n").encode())
            elif (off_axis > 50) :
                print ("turn left8")
                uart.write (("/turn/run 50 0.3 \n").encode())
            else :
                print ("go stright6")
                uart.write (("/goStraight/run 70 \n").encode())
        else :
            if (off_axis < -15) :
                count = 0
                print ("turn right7")
                uart.write (("/turn/run 50 -0.3 \n").encode())
            elif (off_axis > 15) :
                count = 0
                print ("turn left8")
                uart.write (("/turn/run 50 0.3 \n").encode())
            else :
                count += 1
                if (count > 3) :
                    print ("stop10")
                    uart.write (("/stop/run \n").encode())
                else :
                    print ("go stright9, count = %f" %(count))
                    uart.write (("/goStraight/run 70 \n").encode())
        time.sleep(0.05)
    if (not find) :
        uart.write (("/stop/run \n").encode())
    print("FPS %f\r\n" % clock.fps())
    #uart.write(("FPS %f\r\n" % clock.fps()).encode())
