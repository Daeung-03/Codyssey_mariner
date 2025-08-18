import random

class DummySensor:
    def __init__(self):
        self.env_values = {}
        self.set_env()
    
    def set_env(self):
        # 지정된 범위 내에서 랜덤 값 생성 및 env_values 업데이트
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)      
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)         
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715) 
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)           
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)