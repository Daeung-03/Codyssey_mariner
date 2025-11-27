import random
import threading
import time
from datetime import datetime


class ParmSensor:
    
    def __init__(self, name):
        self.name = name
        self.temperature = 0
        self.humidity = 0
        self.illuminance = 0
        
        self.lock = threading.Lock()
    
    def SetData(self):
        with self.lock:
            self.temperature = random.randint(20, 30)
            self.illuminance = random.randint(5000, 10000)
            self.humidity = random.randint(40, 70)
    
    def GetData(self):
        with self.lock:
            return self.temperature, self.illuminance, self.humidity


def sensor_worker(sensor):
    while True:
        sensor.SetData()
        temp, light, humi = sensor.GetData()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} {sensor.name} - temp {temp:02d}, light {light:05d}, humi {humi:02d}")
        time.sleep(10)

def main():
    sensors = [ParmSensor(f"Parm-{i}") for i in range(1, 6)]

    threads = []
    for sensor in sensors:
        thread = threading.Thread(target=sensor_worker, args=(sensor,))
        thread.daemon = True 
        thread.start()
        threads.append(thread)

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")

if __name__ == "__main__":
    main()