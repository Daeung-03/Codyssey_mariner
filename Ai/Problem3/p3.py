import random
import threading
import time
from datetime import datetime
import mysql.connector
from mysql.connector import pooling
import matplotlib.pyplot as plt
from collections import defaultdict

class SensorQueue:
    
    def __init__(self):
        self.items = []
        self.head = 0
        self.tail = 0 
        self.lock = threading.Lock()
    
    def push(self, item):
        with self.lock:
            self.items.append(item)
            self.tail += 1
        
        return True
    
    def pop(self):
        with self.lock:
            if self.head == self.tail:
                return None
            
            item = self.items[self.head]
            self.head += 1
            
            return item
    
    def empty(self):
        with self.lock:
            return self.head >= self.tail
    

class ParmSensor:
    
    def __init__(self, name, sensor_queue):
        self.name = name
        self.temperature = 0
        self.humidity = 0
        self.illuminance = 0
        self.sensor_queue = sensor_queue
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

    
def sensor_worker(sensor, running):
    while running['active']:
        sensor.SetData()
        temp, light, humi = sensor.GetData()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} {sensor.name} - temp {temp:02d}, light {light:05d}, humi {humi:02d}")
        # 큐에 데이터 저장 
        sensor.sensor_queue.push({
            'timestamp': timestamp,
            'temperature': temp,
            'illuminance': light,
            'humidity': humi
        })
        time.sleep(10)

def queue_processor(sensor_queue, db_pool, running):
    while running['active'] or not sensor_queue.empty():
        if not sensor_queue.empty():
            
            data = sensor_queue.pop()
            
            if data:
                
                # DB에 저장
                insert_sensor_data(
                    db_pool,
                    data['timestamp'],
                    data['temperature'],
                    data['illuminance'],
                    data['humidity']
                )
        
        time.sleep(1)  # 1초마다 확인
    
    print("✓ 큐 프로세서 종료!")

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

def get_sensor_data(db_pool):
    conn = None
    data = []
    
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT id, input_time, temperature, illuminance, humidity
        FROM parm_data
        ORDER BY input_time
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        
    except Exception as e:
        print(f"✗ DB 조회 오류: {e}")
    finally:
        if conn:
            conn.close()
    
    return data

def draw_temperature_graph(db_pool):
    """시간별 온도 평균 그래프 그리기"""
    data = get_sensor_data(db_pool)
    
    if not data:
        print("데이터가 없습니다!")
        return
    
    # 시간별로 온도 데이터 그룹화
    time_temp = defaultdict(list)
    
    for row in data:
        data_id, input_time, temperature, illuminance, humidity = row
        time_key = input_time.strftime('%H:%M:%S')
        time_temp[time_key].append(temperature)
    
    # 평균 계산
    times = sorted(time_temp.keys())
    avg_temps = [sum(time_temp[t]) / len(time_temp[t]) for t in times]
    
    # 그래프 그리기
    plt.figure(figsize=(12, 6))
    plt.plot(times, avg_temps, marker='o', linewidth=2, markersize=8)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Average Temperature (°C)', fontsize=12)
    plt.title('Smart Farm - Average Temperature Over Time', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    print(f"✓ 그래프 생성 완료! (총 {len(times)}개 시간대)")

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
    
    sensor_queue = SensorQueue()

    sensors = [ParmSensor(f"Parm-{i}", sensor_queue) for i in range(1, 6)]

    running = {'active': True}
    queue_thread = threading.Thread(target=queue_processor, args=(sensor_queue, db_pool, running))
    queue_thread.start()

    threads = []
    for sensor in sensors:
        thread = threading.Thread(target=sensor_worker, args=(sensor, running))
        thread.daemon = True 
        thread.start()
        threads.append(thread)

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\n\n프로그램을 종료합니다...")
    finally:
        running['active'] = False
        queue_thread.join()
        print("✓ 모든 데이터 처리 완료!")
        draw_temperature_graph(db_pool)

if __name__ == "__main__":
    main()