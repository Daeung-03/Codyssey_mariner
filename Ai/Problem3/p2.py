import random
import threading
import time
from datetime import datetime
import mysql.connector
from mysql.connector import pooling


class ParmSensor:
    
    def __init__(self, name, db_pool):
        self.name = name
        self.temperature = 0
        self.humidity = 0
        self.illuminance = 0
        self.db_pool = db_pool
        self.lock = threading.Lock()
        
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
        insert_sensor_data(sensor.db_pool, timestamp, temp, light, humi)
        time.sleep(10)

def insert_sensor_data(db_pool, timestamp, temperature, illuminance, humidity):
    conn = None
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO parm_data (input_time, temperature, illuminance, humidity)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (timestamp, temperature, illuminance, humidity))
        conn.commit()
        cursor.close()
        
    except Exception as e:
        print(f"✗ DB 삽입 오류: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def main():
    try:
        db_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="sensor_pool",
            pool_size=10,
            host="localhost",
            database="codyssey_p3",
            user="root",
            password=open("password.txt", "r").read().strip()
        )
        print("✓ DB 연결 성공!")
    except Exception as e:
        print(f"✗ DB 연결 실패: {e}")
        return

    sensors = [ParmSensor(f"Parm-{i}", db_pool) for i in range(1, 6)]

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