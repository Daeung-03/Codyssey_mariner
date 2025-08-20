import zipfile
import itertools
import string
import time
import multiprocessing as mp
from functools import partial

zip_file_path = "emergency_storage_key.zip"    
    
def test_password(zip_path, password):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # 첫 번째 파일만 테스트해서 속도 향상
            name = zip_file.namelist()[0]
            zip_file.testzip()
            zip_file.open(name, pwd=password.encode('utf-8')).read(1)
        return True
    except:
        return False


def test_password_batch(zip_path, password_list):
    """
    패스워드 리스트를 배치로 테스트
    """
    for password in password_list:
        if test_password(zip_path, password):
            return password
    return None
    
def unlock_zip(zip_path, batch_size=80000, num_processes=6):
    charset = string.ascii_lowercase + string.digits
    
    # 패스워드 생성기를 배치로 나누기
    password_generator = (''.join(p) for p in itertools.product(charset, repeat=6))
    start_time = time.time()
    print(f"시작시간: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    tested = 0

    with mp.Pool(processes=num_processes) as pool:
        while True:
            # 배치 크기만큼 패스워드 생성
            bulk = list(itertools.islice(password_generator, batch_size * num_processes))
            if not bulk:
                break
                
            sub_batches = [bulk[(i*batch_size):(i+1)*batch_size] for i in range(num_processes)]
                
            worker = partial(test_password_batch, zip_path)
            results = pool.map(worker, sub_batches)
            tested += 6
            
            # 결과 확인
            for result in results:
                if result:
                    return result
                
            elapsed = time.time() - start_time
            print(f"경과시간: {elapsed}, 반복횟수: {tested}")

    
    print("패스워드를 찾지 못했습니다.")
    return None

def main():
    found = unlock_zip(zip_file_path)

    with open('passward.txt', 'w', encoding='utf-8') as f:
        f.write(found)

    print(found)

if __name__ == '__main__':
    main()