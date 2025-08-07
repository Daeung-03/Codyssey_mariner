import json

def loading():
    with open("mission_computer_main.log", "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines

def print_log(lines):
    log_list = []
    for line in lines[1:]:
        parts = line.strip().split(",")
        if len(parts) == 3:
            log_list.append([parts[0], parts[2]])

    print(log_list)
    # 타임스태프 기준 출력
    log_list.sort(key=lambda x: x[0], reverse=True)
    print("----sorted----")
    print(log_list)

    return log_list

def make_dict(log_list):
    log_dict = {data[0]: data[1] for data in log_list}
    with open("mission_computer_main.json", "w", encoding="utf-8") as f:
        json.dump(log_dict, f, indent=2)

def make_danger(lines):
    keywords = ["explosion", "leak", "high temperature", "Oxygen"]
    danger_log = list()

    for data in lines:
        if any(keyward in data for keyward in keywords):
            danger_log.append(data.strip() + "\n")

    with open("danger.log", "w", encoding="utf-8") as f:
        for line in danger_log:
            f.write(line)

def search_logs(keyword):
    # JSON 파일 열고 딕셔너리 로드
    with open("mission_computer_main.json", "r", encoding="utf-8") as f:
        log_dict = json.load(f)

    # 검색어 소문자화(대소문자 구분 없이 검색하도록)
    keyword_lower = keyword.lower()

    # 포함되는 로그 출력
    found = False
    for timestamp, message in log_dict.items():
        if keyword_lower in message.lower():
            print(f"{timestamp}: {message}")
            found = True

    if not found:
        print(f"'{keyword}'을(를) 포함하는 로그가 없습니다.")

def main():
    try:
        origin_data = loading()
        make_danger(origin_data)
        sorted_data = print_log(origin_data)
        make_dict(sorted_data)

        if input("특정 키워드 검색하려면 1입력. ") == "1":
            search_logs(input("키워드 입력"))

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except UnicodeDecodeError:
        print("디코딩 오류가 발생했습니다.")
    except json.JSONDecodeError:
        print("JSON 파일 내용이 올바르지 않습니다.")
    except Exception as e:
        print(f"알 수 없는 오류: {e}")

if __name__ == "__main__":
    main()