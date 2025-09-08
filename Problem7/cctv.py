import zipfile
import os
import cv2

target = 'cctv.zip'
path = 'CCTV'

def unzip_cctv(target, path):
    with zipfile.ZipFile(target, 'r') as zip_ref:
        zip_ref.extractall(path)

def get_image_files(folder):
    img_ext = ('.jpg', '.jpeg', '.png', '.bmp', '.svg')
    all_files = os.listdir(folder)
    image_files = [f for f in all_files if f.lower().endswith(img_ext)]
    return image_files

def show_image(image_files, folder):
    if not image_files:
        print("이미지 파일이 없습니다.")
        return
    
    current_idx = 0
    title = 'CCTV Image Viewer'
    
    while True:
        # 현재 이미지 파일 경로 생성
        img_path = os.path.join(folder, image_files[current_idx])
        
        # 이미지 읽기 및 표시
        img = cv2.imread(img_path)
        if img is not None:
            cv2.imshow(title, img)
            print(f"현재 이미지: {image_files[current_idx]} ({current_idx + 1}/{len(image_files)})")
        
        # 키 입력 대기 (0은 무한대기)
        key = cv2.waitKeyEx(0)
        print(f"눌린 키: {key}")
        
        # 오른쪽 방향키(windows, mac, ubuntu)
        if key in [0x270000, 63235, 65363]:
            current_idx = (current_idx + 1) % len(image_files)
        
        # 왼쪽 방향키(windows, mac, ubuntu)
        elif key in [0x250000, 63234, 65361]:
            current_idx = (current_idx - 1) % len(image_files)
        
        # ESC키
        elif key == 27:
            break
    
    cv2.destroyAllWindows()

def detect_person(image):
    # HOG 디스크립터 초기화, winSize, blockSize, blockStride, cellSize, nbins
    hog = cv2.HOGDescriptor()
    # 기본 사람 감지 모델 설정
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    boxes, weights = hog.detectMultiScale(image, hitThreshold=-0.5, winStride=(4,4), padding=(32, 32), scale=1.03)
    print(len(boxes))
    return len(boxes) > 0  # 감지된 사람이 있으면 True

def search_people_in_images(image_files, folder):
    if not image_files:
        print("이미지 파일이 없습니다.")
        return
    
    title = 'CCTV People Detection'
    people = 0
    
    print("사람 감지 시작...")
    print("사용법: 엔터키 = 다음 검색 계속, ESC = 종료")
    
    for i, filename in enumerate(image_files):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path)
        
        if img is None:
            continue
            
        print(f"검색 중... {filename} ({i+1}/{len(image_files)})")
        
        # 사람 감지 실행
        if detect_person(img):
            people += 1
            print(f"🔍 사람 발견! {filename}")
            
            # 이미지 화면에 표시
            cv2.imshow(title, img)
            
            # 엔터키 대기
            while True:
                key = cv2.waitKey(0)
                if key == 13:    # 엔터키: 다음 검색 계속
                    break
                elif key == 27:  # ESC키: 종료
                    cv2.destroyAllWindows()
                    print(f"검색 중단됨. 총 {people}명 발견.")
                    return
    
    # 모든 검색 완료
    cv2.destroyAllWindows()
    print(f"검색종료. 총 {people}장의 이미지에서 사람을 발견했습니다.")


def main():
    unzip_cctv(target, path)
    image_files = get_image_files(path)
    search_people_in_images(image_files, path)
    # show_image(image_files, path) # 방향키 사진 검색

if __name__ == "__main__":
    main()