from pyrplidar import PyRPlidar
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
    print(count, scan.angle, scan.distance)
    if count == 10: break

lidar.stop()
lidar.set_motor_pwm(0)

lidar.disconnect()

























#import numpy as np
#import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation

#fig, ax = plt.subplots()

#x = np.linspace(1, 100, 100)
#y = np.random.randint(1, 100, size=100)  # Инициализация y
#line, = ax.plot(x, y)

#def animation(i):
    #y = np.random.randint(1, 100, size=100)  # Обновление y
    #line.set_ydata(y)  # Обновление данных линии
    #return line,  # Возвращаем линию для обновления

#an = FuncAnimation(fig, animation, frames=100, interval=50, blit=True)

#plt.xlabel('Ось х')  # Подпись для оси х
#plt.ylabel('Ось y')  # Подпись для оси y
#plt.title('Первый график')  # Название
#plt.show()