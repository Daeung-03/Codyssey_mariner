import sounddevice as sd
import numpy as np
import soundfile as sf
import os
from datetime import datetime
import threading
import whisper
import csv


def create_records_folder():
    if not os.path.exists('records'):
        os.makedirs('records')
        print('records 폴더를 생성했습니다.')
    else:
        return


def create_filename():
    now = datetime.now()
    filename = now.strftime('%Y%m%d-%H%M%S')
    return filename


def record_audio(sample_rate=44100):
    print('녹음을 시작합니다... (Enter키를 누르면 종료)')

    stop_event = threading.Event()

    # 키 입력 대기 스레드
    def wait_for_input():
        input()  # Enter키 대기
        stop_event.set()  # 종료 신호
        print('\n녹음 종료 신호를 받았습니다...')

    # 키 입력 스레드 시작
    input_thread = threading.Thread(target=wait_for_input)
    input_thread.daemon = True  # 메인 프로그램 종료 시 함께 종료
    input_thread.start()

    # 동적 녹음 시작
    audio_chunks = []  # 녹음 조각들을 저장할 리스트
    chunk_size = int(3 * sample_rate)  # 0.1초씩 나누어 녹음

    while not stop_event.is_set():
        # 0.1초 분량 녹음
        chunk = sd.rec(
            chunk_size, samplerate=sample_rate, channels=1, dtype='float64'
        )
        sd.wait()  # 해당 chunk 녹음 완료 대기
        audio_chunks.append(chunk)

    # 모든 chunk들을 하나로 합치기
    if audio_chunks:
        audio_data = np.concatenate(audio_chunks)
        print(f'총 {len(audio_data) / sample_rate:.2f}초 녹음 완료')
        return audio_data, sample_rate
    else:
        print('녹음된 데이터가 없습니다.')
        return None, sample_rate


def save_audio_file(audio_data, sample_rate):
    if audio_data is None:
        print('저장할 오디오 데이터가 없습니다.')
        return None

    filename = create_filename()
    filepath = os.path.join('records', f'{filename}.wav')

    # soundfile을 사용해서 WAV 파일로 저장
    sf.write(filepath, audio_data, sample_rate)

    print(f'오디오 파일이 저장되었습니다: {filepath}')
    return filename  # STT 처리 시 사용할 파일명 반환


def get_audio_files():
    if not os.path.exists('records'):
        print('records 폴더가 존재하지 않습니다.')
        return []

    audio_files = []
    for filename in os.listdir('records'):
        if filename.endswith('.wav'):
            filepath = os.path.join('records', filename)
            audio_files.append((filename, filepath))

    print(f'총 {len(audio_files)}개의 음성 파일을 발견했습니다.')
    return audio_files


def STT(audio_file_path):
    try:
        print(f'STT 처리 중: {audio_file_path}')

        # Whisper 모델 로드 (base 모델 사용)
        model = whisper.load_model('base')

        # 음성 파일 transcribe (word_timestamps=True로 단어별 타임스탬프 제공)
        result = model.transcribe(audio_file_path, word_timestamps=True)

        # 세그먼트별 결과 추출
        transcript_data = []
        for segment in result['segments']:
            start_time = segment['start']  # 시작 시간 (초)
            end_time = segment['end']  # 종료 시간 (초)
            text = segment['text'].strip()  # 인식된 텍스트

            transcript_data.append(
                {'start_time': start_time, 'end_time': end_time, 'text': text}
            )

        print(f'STT 완료: {len(transcript_data)}개 세그먼트 처리')
        return transcript_data

    except Exception as e:
        print(f'STT 처리 오류: {e}')
        return []


def save_transcript_to_csv(transcript_data, audio_filename):
    if not transcript_data:
        print('저장할 STT 데이터가 없습니다.')
        return

    csv_filename = audio_filename.replace('.wav', '.csv')
    csv_filepath = os.path.join('records', csv_filename)

    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['시작시간(초)', '종료시간(초)', '인식된텍스트']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 헤더 작성
        writer.writeheader()

        # 데이터 작성
        for item in transcript_data:
            writer.writerow(
                {
                    '시작시간(초)': f'{item["start_time"]:.2f}',
                    '종료시간(초)': f'{item["end_time"]:.2f}',
                    '인식된텍스트': item['text'],
                }
            )

    print(f'CSV 파일 저장 완료: {csv_filepath}')


def all_audio_files():
    audio_files = get_audio_files()

    if not audio_files:
        print('처리할 음성 파일이 없습니다.')
        return

    for filename, filepath in audio_files:
        print(f'\n=== {filename} 처리 중 ===')

        transcript_data = STT(filepath)

        if transcript_data:
            save_transcript_to_csv(transcript_data, filename)
        else:
            print(f'{filename} STT 처리 실패')


def main():
    create_records_folder()

    while True:
        print('1. 음성 녹음')
        print('2. STT 처리 (기존 음성 파일들)')
        print('3. 종료')

        choice = input('메뉴를 선택하세요 (1/2/3): ').strip()

        if choice == '1':
            print('\n[음성 녹음 시작]')
            audio_data, sample_rate = record_audio()

            if audio_data is not None and audio_data.size > 0:
                filename = save_audio_file(audio_data, sample_rate)
                print(f'녹음 완료: {filename}.wav')
            else:
                print('녹음된 데이터가 없습니다.')

        elif choice == '2':
            print('\n[STT 처리 시작]')
            all_audio_files()

        elif choice == '3':
            print('프로그램을 종료합니다.')
            break

        else:
            print('잘못된 선택입니다. 1, 2, 3 중에서 선택해주세요.')


if __name__ == '__main__':
    main()
