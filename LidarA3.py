from pyrplidar import PyRPlidar
import matplotlib.pyplot as plt
import numpy as np
import math
import threading
import time
from matplotlib.animation import FuncAnimation


x_data = []
y_data = []
lock = threading.Lock()
stop_lidar = False  # Флаг для остановки лидара


# Функция для сбора данных с лидара
def lidar_scan():
    global x_data, y_data, stop_lidar

    lidar = PyRPlidar()

    try:
        lidar.connect(port="COM4", baudrate=256000, timeout=3)
        lidar.set_motor_pwm(500)
        time.sleep(2)

        scan_generator = lidar.start_scan_express(4)

        for scan in scan_generator():
            if stop_lidar:
                break

            new_x = scan.distance * math.sin(math.radians(scan.angle))
            new_y = scan.distance * math.cos(math.radians(scan.angle))

            with lock:
                x_data.append(new_x)
                y_data.append(new_y)

                if len(x_data) > 1000:
                    x_data = x_data[-1000:]
                    y_data = y_data[-1000:]

    except Exception as e:
        print(f"Ошибка работы с лидаром: {e}")

    finally:
        print("Остановка лидара...")
        lidar.stop()
        lidar.set_motor_pwm(0)
        lidar.disconnect()
        print("Лидар отключен.")


# Функция обновления графика
def update(frame):
    with lock:
        ax.clear()
        ax.scatter(x_data, y_data, c='blue', s=5)
        ax.set_xlim(-10000, 10000)
        ax.set_ylim(-10000, 10000)
        ax.set_xlabel('Ось X')
        ax.set_ylabel('Ось Y')
        ax.set_title('Облако точек')


#остановка лидара при закрытии окна
def on_close(event):
    global stop_lidar
    stop_lidar = True  #перевожу флаг чтобы он сработал 30 строчке
    print("Закрытие окна. Остановка лидара...")



threading.Thread(target=lidar_scan, daemon=True).start()

fig, ax = plt.subplots()

#обработчик закрытия окна
fig.canvas.mpl_connect('close_event', on_close)


ani = FuncAnimation(fig, update, interval=100, cache_frame_data=False)
plt.show()
