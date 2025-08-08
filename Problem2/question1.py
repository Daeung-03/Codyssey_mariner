import numpy as np
import pickle


def loading():
    # 파일 읽고 출력
    with open(
        'mars_base/Mars_Base_Inventory_List.csv', 'r', encoding='utf-8'
    ) as f:
        lines = f.readlines()
    [print(row, end='') for row in lines[1:]]
    # 파싱 -> 리스트 객체
    log_list = list()
    for line in lines[1:]:
        row = line.strip().split(',')
        log_list.append(row)
    # 정렬
    log_list.sort(key=lambda x: x[4], reverse=True)
    # 별도  출력
    print('----filterd----')
    filterd_data = [row for row in log_list if float(row[4]) >= 0.7]
    [print(','.join(line)) for line in filterd_data]
    # numpy 활용하여 csv파일 저장
    arr = np.array(filterd_data, dtype=str)
    np.savetxt('Mars_Base_Inventory_danger.csv', arr, fmt='%s', delimiter=',')
    # 이진파일 저장 후 출력
    print('----binary 출력----')
    with open('Mars_Base_Inventory_List.bin', 'wb') as f:
        pickle.dump(filterd_data, f, pickle.HIGHEST_PROTOCOL)

    with open('Mars_Base_Inventory_List.bin', 'rb') as f:
        loaded_arr = pickle.load(f)

    [print(','.join(line)) for line in loaded_arr]


def main():
    loading()


if __name__ == '__main__':
    main()
