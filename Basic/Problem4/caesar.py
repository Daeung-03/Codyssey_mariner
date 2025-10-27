from collections import deque
import string


def caesar_cipher_decode(target_text, key):
    plain = string.ascii_lowercase
    cipher = deque(plain)
    cipher.rotate(-key)

    decode_map = {ori: dec for ori, dec in zip(cipher, plain)}
    decode_map.update(
        {ori.upper(): dec.upper() for ori, dec in zip(cipher, plain)}
    )

    answer = ''.join(decode_map.get(ch, ch) for ch in target_text)
    print(f'shift {key}: {answer}')


def main():
    try:
        with open('password.txt', 'r', encoding='utf-8') as f:
            cipher = f.readline()

        print('올바른 해석을 찾으시오: ')

        for key in range(1, 27):
            caesar_cipher_decode(cipher, key)

        select = input('해석이 되는 숫자는?: ')
        with open('result.txt', 'w', encoding='utf-8') as f:
            f.write(select)

        print('저장 완료')
    except (KeyboardInterrupt, EOFError):
        print('강제 종료 되었습니다.')
        exit()
    except FileNotFoundError:
        print('파일이 존재하지 않습니다.')
        exit()
    except Exception as e:
        print('에러 발생: {e}')
        exit()


if __name__ == '__main__':
    main()
