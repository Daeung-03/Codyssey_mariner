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
        
        # 오른쪽 방향키
        if key == 0x270000 or key == 63235:
            current_idx = (current_idx + 1) % len(image_files)
        
        # 왼쪽 방향키
        elif key == 0x250000 or key == 63234:
            current_idx = (current_idx - 1) % len(image_files)
        
        # ESC키
        elif key == 27:
            break
    
    cv2.destroyAllWindows()

def main():
    unzip_cctv(target, path)
    image_files = get_image_files(path)
    show_image(image_files, path)

if __name__ == "__main__":
    main()