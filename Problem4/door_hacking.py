import zipfile
import itertools
import string
import time
from datetime import datetime
import multiprocessing as mp

zip_file_path = 'emergency_storage_key.zip'


def test_password(zip_path, password):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # 첫 번째 파일만 테스트해서 속도 향상
            name = zip_file.namelist()[0]
            with zip_file.open(name, pwd=password.encode('utf-8')) as file:
                file.read(1)
        return True

    except IndexError:
        raise Exception('ZIP 파일이 비어 있습니다.')

    except FileNotFoundError:
        raise ('파일을 찾을 수 없습니다.')

    except:
        return False


def test_password_batch(args):
    zip_path, password_list = args
    for password in password_list:
        if test_password(zip_path, password):
            return password

    return None


def unlock_zip(zip_path, batch_size=15000, num_processes=6):
    charset = string.ascii_lowercase + string.digits

    # 패스워드 생성기를 배치로 나누기
    password_generator = (
        ''.join(p) for p in itertools.product(charset, repeat=6)
    )
    start_time = time.time()
    print(f'시작시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S KST")}')
    tested = 0
    try:
        with mp.Pool(processes=num_processes) as pool:
            while True:
                batch = list(
                    itertools.islice(
                        password_generator, batch_size * num_processes
                    )
                )
                if not batch:
                    break

                tasks = [(zip_path, batch)]

                results = pool.map(test_password_batch, tasks)

                for result in results:
                    if result:
                        return result

                elapsed = time.time() - start_time
                tested += num_processes

                print(f'경과시간: {elapsed}, 반복횟수: {tested}')

        print('패스워드를 찾지 못했습니다.')
        return None
    except mp.ProcessError:
        raise Exception('멀티 프로세싱 오류')  # 프로세스 생성/관리 오류

    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
        raise Exception('강제 종료')


def main():
    try:
        found = unlock_zip(zip_file_path)

        with open('password/password.txt', 'w', encoding='utf-8') as f:
            f.write(found)

        print(found)
    except Exception as e:
        print(f'에러 발생: {e}')
        exit()


if __name__ == '__main__':
    main()
