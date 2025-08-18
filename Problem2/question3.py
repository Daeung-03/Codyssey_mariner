import numpy as np

def loading():
    dtype_parts = [('parts', 'U50'), ('strength', 'f8')]

    arr1 = np.genfromtxt('mars_base/mars_base_main_parts-001.csv', delimiter=',', skip_header=1, dtype=dtype_parts)
    arr2 = np.genfromtxt('mars_base/mars_base_main_parts-002.csv', delimiter=',', skip_header=1, dtype=dtype_parts)
    arr3 = np.genfromtxt('mars_base/mars_base_main_parts-003.csv', delimiter=',', skip_header=1, dtype=dtype_parts)

    parts = np.concatenate([arr1, arr2, arr3])

    part_names = np.unique(parts['parts'])
    avg_list = []
    for name in part_names:
        strengths = parts['strength'][parts['parts'] == name]
        mean_strength = np.mean(strengths)
        mean_strength = round(mean_strength, 3)
        avg_list.append((name, mean_strength))

    avg_arr = np.array(avg_list, dtype=[('parts', 'U50'), ('mean_strength', 'f8')])

    filtered = avg_arr[avg_arr['mean_strength'] < 50]
    for part, mean_strength in filtered:
        print(f"('{part}', {mean_strength:.3f})")
    
    try:
        # 헤더 문자열 생성
        header = "parts, mean_strength"
        # savetxt: 구조화 배열은 2차원 배열 아닌 경우 field값을 자리에 맞게 적어야 함
        np.savetxt('parts_to_work_on.csv', filtered, 
                fmt='%s,%.3f', delimiter=',', header=header, comments='')
        print("저장 완료!")
    except Exception:
        raise Exception("저장 실패")


def bonus():
    dtype_parts = [('parts', 'U50'), ('strength', 'f8')]
    parts2 = np.genfromtxt('parts_to_work_on.csv', 
                       delimiter=',', 
                       skip_header=1, 
                       dtype=dtype_parts)
    print("\n=== parts2 ===")
    for part, streng in parts2:
        print(f"('{part}', {streng:.3f})")

    streng_row = np.char.mod('%.3f', parts2['strength'])
    parts3 = np.column_stack((parts2['parts'], streng_row))
    parts3 = parts3.T
    
    print("\n=== parts3 ===")
    print(parts3)

def main():
    try:
        loading()
        bonus()
    except FileNotFoundError:
        print("파일 로딩 실패")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()