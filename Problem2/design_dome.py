import numpy as np
import math
import sys

MAX_INT = sys.maxsize

def sphere_area(diameter, material, thickness = 1 ):
    check_valid(diameter, material)
    name = {'gls': '유리', 'alu': '알루미늄', 'cars': '탄소강'}
    density = {'gls': 2.4, 'alu': 2.7, 'cars': 7.85}
    global area 
    area = 3 * math.pi * ((diameter/2)**2)
    volume = (4/3) * math.pi * (((diameter * 100)/2)**3) 
    global weightness 
    weightness = (volume * density[material.lower()] * 0.38)/1000

    print(f"재질⇒{name[material.lower()]}, 지름⇒{diameter}, 두께⇒1, 면적⇒{area: .3f}, 무게⇒{weightness: .3f} kg")

def check_valid(diameter, material):
    if material.lower() not in ['gls', 'alu', 'cars']:
        raise ValueError("You must choose from given values")
    
    if diameter <= 0:
        raise ValueError("Diameter can't be negative and zero")

    if diameter > MAX_INT:
        raise ValueError(f"limit of diameter is {MAX_INT}")

def main():
    while True:
        try:
            print('You want to quit, press q')
            global diameter
            diameter = input("Enter diameter: ").strip()
            if diameter.lower() == 'q':
                break
            global material
            material = input("choose material(Gls, Alu, CarS): ").strip()
            if material.lower() == 'q':
                break
            
            sphere_area(float(diameter), material)
            
        except ValueError as ve:
            print(f"Invalid diameter: {ve}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()