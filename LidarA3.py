from pyrplidar import PyRPlidar
import matplotlib.pyplot as plt
import time
import math

lidar = PyRPlidar()
lidar.connect(port="COM4", baudrate=256000, timeout=3)
# Windows : "COM4"

info = lidar.get_info()
print("info :", info)

x = []
y = []

lidar.set_motor_pwm(500)
time.sleep(2)

scan_generator = lidar.start_scan_express(4)

for count, scan in enumerate(scan_generator()):

    x.append(scan.distance * math.sin(math.radians(scan.angle)))
    y.append(scan.distance * math.cos(math.radians(scan.angle)))
    print(count, scan)
    if count == 10000:
        lidar.stop()
        lidar.set_motor_pwm(0)
        lidar.disconnect()
        break


print("Переведенные координаты по оси X:",x)
print("Переведенные координаты по оси Y:",y)


plt.figure()
plt.scatter(x,y)

plt.xlabel('Ось х')
plt.ylabel('Ось y')
plt.title('Облако точек')
plt.pause(.1)
plt.show()


