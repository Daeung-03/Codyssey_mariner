import random
from datetime import datetime
import json
import time
import threading
import platform
import psutil 
import os
import configparser
import multiprocessing


class DummySensor:
    def __init__(self):
        self.env_values = {}
        self.set_env()
    
    def set_env(self):
        # 지정된 범위 내에서 랜덤 값 생성 및 env_values 업데이트
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)      
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)         
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715) 
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1),2)           
        self.env_values['mars_base_internal_oxygen'] = random.randint(4, 7)

    def get_env(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S KST')

        log_line = (
            f"{current_time}, "
            f"화성 기지 내부 온도: {self.env_values['mars_base_internal_temperature']}도, "
            f"화성 기지 외부 온도: {self.env_values['mars_base_external_temperature']}도, "
            f"화성 기지 내부 습도: {self.env_values['mars_base_internal_humidity']}%, "
            f"화성 기지 외부 광량: {self.env_values['mars_base_external_illuminance']}W/m2, "
            f"화성 기지 내부 이산화탄소 농도: {self.env_values['mars_base_internal_co2']}%, "
            f"화성 기지 내부 산소 농도: {self.env_values['mars_base_internal_oxygen']}%\n"
        )

        with open('log_que1.txt', 'a', encoding='utf-8') as f:
            f.write(log_line)

        return self.env_values

class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }
    
        self.history = {
                'mars_base_internal_temperature': [],
                'mars_base_external_temperature': [],
                'mars_base_internal_humidity': [],
                'mars_base_external_illuminance': [],
                'mars_base_internal_co2': [],
                'mars_base_internal_oxygen': []
            }
        
        self.loop_count = 0
        self.ds = DummySensor()
    
    def get_sensor_data(self, stop_event):
        print("시스템 시작. 종료 원하면 q누르고 엔터")

        while not stop_event.is_set():
            # 센서 값 업데이트 (새 랜덤 값 생성)
            self.ds.set_env()
            # 센서 값과 log_line 가져와 env_values에 저장 및 출력
            self.env_values = self.ds.get_env()
            
            formatted_values = {
                'mars_base_internal_temperature': f"{self.env_values['mars_base_internal_temperature']}도",
                'mars_base_external_temperature': f"{self.env_values['mars_base_external_temperature']}도",
                'mars_base_internal_humidity': f"{self.env_values['mars_base_internal_humidity']}%",
                'mars_base_external_illuminance': f"{self.env_values['mars_base_external_illuminance']} W/m²",
                'mars_base_internal_co2': f"{self.env_values['mars_base_internal_co2']}%",
                'mars_base_internal_oxygen': f"{self.env_values['mars_base_internal_oxygen']}%"
            }

            print(json.dumps(formatted_values, indent=4, ensure_ascii=False))

            # history에 값 추가
            for key in self.env_values:
                self.history[key].append(self.env_values[key])
            
            # 루프 카운터 증가
            self.loop_count += 1

            if self.loop_count >= 3:
                avg_line = self.calculate_averages()
                print(f"5분 평균 값: {avg_line}")
                # history와 카운터 초기화
                for key in self.history:
                    self.history[key] = []
                self.loop_count = 0
            
            # 5초 대기 (중단 이벤트 체크와 함께)
            start_time = time.time()
            while time.time() - start_time < 5 and not stop_event.is_set():
                time.sleep(0.1)

        print("System stopped….")

    def calculate_averages(self):
        # 각 키별 평균 계산 (float으로 유지, 소수점 2자리 반올림)
        avgs = {}
        for key in self.history:
            values = self.history[key]
            if values:
                avg = round(sum(values) / len(values), 2)
                avgs[key] = avg
        
        avg_line = (
            f"화성 기지 내부 온도: {avgs['mars_base_internal_temperature']}도, "
            f"화성 기지 외부 온도: {avgs['mars_base_external_temperature']}도, "
            f"화성 기지 내부 습도: {avgs['mars_base_internal_humidity']}%, "
            f"화성 기지 외부 광량: {avgs['mars_base_external_illuminance']} W/m², "
            f"화성 기지 내부 이산화탄소 농도: {avgs['mars_base_internal_co2']}%, "
            f"화성 기지 내부 산소 농도: {avgs['mars_base_internal_oxygen']}%"
        )
        return avg_line
    
    def get_mission_computer_info(self,stop_event):
        config = configparser.ConfigParser()
        if not os.path.exists('setting.txt'):
            with open('setting.txt', 'w', encoding='utf-8') as f:
                f.write('[info]\n운영체계=1\n운영체계 버전=1\nCPU 타입=1\nCPU 코어 수=1\n메모리 크기=1\n')
                f.write('[load]\nCPU 실시간 사용량=1\n메모리 실시간 사용량=1\n')
        config.read('setting.txt')
        while not stop_event.is_set():
            all_info = {
                '운영체계': platform.system(),
                '운영체계 버전': platform.version(),
                'CPU 타입': platform.processor(),
                'CPU 코어 수': psutil.cpu_count(logical=True),
                '메모리 크기': f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"
            }

            info = {}
            for key in all_info:
                try:
                    if config.getboolean('info', key):
                        info[key] = all_info[key]
                except (configparser.NoSectionError, configparser.NoOptionError):
                    pass  # 섹션/키 없으면 무시
                except(ValueError):
                    raise ValueError('setting.txt가 잘못되어있습니다.')
            print(json.dumps(info, ensure_ascii=False, indent=4))
            start_time = time.time()
            while time.time() - start_time < 5 and not stop_event.is_set():
                time.sleep(0.1)
    
    def get_mission_computer_load(self,stop_event):
        config = configparser.ConfigParser()
        config.read('setting.txt')

        while not stop_event.is_set():
            all_load = {
                'CPU 실시간 사용량': f"{psutil.cpu_percent(interval=1)}%",
                '메모리 실시간 사용량': f"{psutil.virtual_memory().percent}%"
            }

            load = {}
            for key in all_load:
                try:
                    if config.getboolean('load', key):
                        load[key] = all_load[key]
                except (configparser.NoSectionError, configparser.NoOptionError):
                    pass
                except(ValueError):
                    raise ValueError('setting.txt가 잘못되어있습니다.')

            print(json.dumps(load, ensure_ascii=False, indent=4))
            start_time = time.time()
            while time.time() - start_time < 5 and not stop_event.is_set():
                time.sleep(0.1)
    
def input_listener(stop_event):
    try:
        while not stop_event.is_set():
            user_input = input().strip().lower()
            if user_input == 'q':
                print("종료 신호를 받았습니다. 모든 프로세스를 종료합니다...")
                stop_event.set()
                break
    except (KeyboardInterrupt, EOFError):
        print("\n강제 종료 신호를 받았습니다. 모든 프로세스를 종료합니다...")
        stop_event.set()

def main():
    try:
        print(os.getpid()) 
        ds = DummySensor()
        ds.set_env()
        print(ds.get_env())

        # stop_event = threading.Event()

        # runComputer = MissionComputer()
        # thread1 = threading.Thread(target=runComputer.get_mission_computer_info, args=(stop_event,), daemon=True)
        # thread2 = threading.Thread(target=runComputer.get_mission_computer_load, args=(stop_event,), daemon=True)
        # thread3 = threading.Thread(target=runComputer.get_sensor_data, args=(stop_event,))

        # input_thread = threading.Thread(target=input_listener, args=(stop_event,), daemon=True)
        # input_thread.start()

        # print("\n미션 컴퓨터 시스템 정보:")
        # thread1.start()
        # print("\n미션 컴퓨터 실시간 부하:")
        # thread2.start()
        # print("MissionComputer 시작 (5초 간격으로 데이터 출력):")
        # thread3.start()
        # thread3.join()

        # try:
        #     while not stop_event.is_set():
        #         time.sleep(0.1)  # CPU 사용률을 낮추기 위한 짧은 대기
        # except KeyboardInterrupt:
        #     print("\n강제 종료 신호를 받았습니다. 모든 프로세스를 종료합니다...")
        #     stop_event.set()

        stop_event = multiprocessing.Event()

        runComputer1 = MissionComputer()
        runComputer2 = MissionComputer()
        runComputer3 = MissionComputer()

        p1 = multiprocessing.Process(target=runComputer1.get_mission_computer_info, args=(stop_event,))
        p2 = multiprocessing.Process(target=runComputer2.get_mission_computer_load, args=(stop_event,))
        p3 = multiprocessing.Process(target=runComputer3.get_sensor_data, args=(stop_event,))

        input_thread = threading.Thread(target=input_listener, args=(stop_event,), daemon=True)
        input_thread.start()

        p1.start()
        p2.start()
        p3.start()

        try:
            while not stop_event.is_set():
                time.sleep(0.1)  # CPU 사용률을 낮추기 위한 짧은 대기
        except KeyboardInterrupt:
            print("\n강제 종료 신호를 받았습니다. 모든 프로세스를 종료합니다...")
            stop_event.set()

        # 모든 프로세스가 종료될 때까지 대기
        p1.join()
        p2.join()
        p3.join()

    except ValueError as ve:
        print(f'{ve}')

if __name__ == '__main__':
    main()