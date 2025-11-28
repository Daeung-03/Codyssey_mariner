class Node:
    
    def __init__(self, data):
        self.data = data
        self.next = None

class linkedlist:
    def __init__(self):
        self.head = None
    
    def insert(self, data, position=None):
        new_node = Node(data)
        
        # 맨 앞에 삽입
        if position == 0 or self.head is None:
            new_node.next = self.head
            self.head = new_node
            print(f"'{data}'을(를) 맨 앞에 추가했습니다.")
            return
        
        # 맨 뒤에 삽입 (position이 None인 경우)
        if position is None:
            if self.head is None:
                self.head = new_node
            else:
                current = self.head
                while current.next is not None:
                    current = current.next
                current.next = new_node
            print(f"'{data}'을(를) 맨 뒤에 추가했습니다.")
            return
        
        # 중간에 삽입
        current = self.head
        count = 0
        while current is not None and count < position - 1:
            current = current.next
            count += 1
        
        if current is None:
            print("리스트 범위를 벗어났습니다.")
            return
        
        new_node.next = current.next
        current.next = new_node
        print(f"'{data}'을(를) 위치 {position}에 추가했습니다.")
    
    def delete(self, index):
        if self.head is None:
            print("리스트가 비어있습니다.")
            return None
        
        # 인덱스가 음수인 경우
        if index < 0:
            print("인덱스는 0 이상이어야 합니다.")
            return None
        
        # 맨 앞 노드를 삭제하는 경우 (index == 0)
        if index == 0:
            self.head = self.head.next
            print(f"인덱스 {index}을(를) 삭제했습니다.")
            return None
        
        # 중간이나 끝 노드를 삭제하는 경우
        current = self.head
        count = 0
        while current.next is not None and count < index - 1:
            current = current.next
            count += 1
        
        # 삭제할 노드가 없는 경우
        if current.next is None:
            print(f"인덱스 {index}이(가) 리스트 범위를 벗어났습니다.")
            return None
        
        deleted_node = current.next
        current.next = deleted_node.next
        print(f"인덱스 {index}을(를) 삭제했습니다.")
        return None
    
    def display(self):
        if self.head is None:
            print("플레이리스트가 비어있습니다.")
            return
        
        current = self.head
        print("\n=== 현재 플레이리스트 ===")
        index = 0
        while current is not None:
            print(f"{index}. {current.data}")
            current = current.next
            index += 1
        print("=" * 30 + "\n")
    
    def is_empty(self):
        return self.head is None

class circularlist:

    def __init__(self):
        self.last = None
        self.current = None

    def insert(self, data, position=None):
        new_node = Node(data)

        if self.last is None:
            self.last = new_node
            new_node.next = new_node
            self.current = new_node
            print(f"'{data}'을(를) 맨 앞에 추가했습니다.")
            return

        if position == 0:
            new_node.next = self.last.next
            self.last.next = new_node
            print(f"'{data}'을(를) 맨 앞에 추가했습니다.")
            return
        
        if position is None:
            new_node.next = self.last.next
            self.last.next = new_node
            self.last = new_node
            print(f"'{data}'을(를) 맨 뒤에 추가했습니다.")
            return

        current = self.last.next 
        count = 0
        
        while count < position - 1:
            current = current.next
            count += 1
            # 한 바퀴 돌아서 다시 첫 노드로 돌아온 경우
            if current == self.last.next and count < position - 1:
                print(f"위치 {position}이(가) 리스트 범위를 벗어났습니다.")
                return
        
        new_node.next = current.next
        current.next = new_node
        
        if current == self.last:
            self.last = new_node
        
        print(f"'{data}'을(를) 위치 {position}에 추가했습니다.")
    
    def delete(self, index):
        """
        특정 인덱스의 노드를 삭제하는 함수 (0-based index)
        """
        if self.last is None:
            print("리스트가 비어있습니다.")
            return None
        
        # 인덱스가 음수인 경우
        if index < 0:
            print("인덱스는 0 이상이어야 합니다.")
            return None
        
        # 노드가 하나만 있는 경우
        if self.last.next == self.last:
            if index == 0:
                deleted_data = self.last.data
                self.last = None
                self.current = None
                print(f"인덱스 {index}의 '{deleted_data}'을(를) 삭제했습니다.")
                return deleted_data
            else:
                print(f"인덱스 {index}이(가) 리스트 범위를 벗어났습니다.")
                return None
        
        # 맨 앞 노드를 삭제하는 경우 (index == 0)
        if index == 0:
            first_node = self.last.next
            deleted_data = first_node.data
            self.last.next = first_node.next
            
            # current가 삭제되는 노드를 가리키고 있었다면 업데이트
            if self.current == first_node:
                self.current = self.last.next
            
            print(f"인덱스 {index}의 '{deleted_data}'을(를) 삭제했습니다.")
            return deleted_data
        
        # 중간이나 끝 노드를 삭제하는 경우
        current = self.last.next
        count = 0
        
        # index-1 번째 노드까지 이동
        while count < index - 1:
            current = current.next
            count += 1
            # 한 바퀴 돌아온 경우
            if current == self.last.next:
                print(f"인덱스 {index}이(가) 리스트 범위를 벗어났습니다.")
                return None
        
        if current.next == self.last.next and count < index - 1:
            print(f"인덱스 {index}이(가) 리스트 범위를 벗어났습니다.")
            return None
        
        deleted_node = current.next
        current.next = deleted_node.next
        
        # 마지막 노드를 삭제한 경우 last 업데이트
        if deleted_node == self.last:
            self.last = current
        
        # current가 삭제되는 노드를 가리키고 있었다면 업데이트
        if self.current == deleted_node:
            self.current = deleted_node.next
        
        print(f"인덱스 {index}을(를) 삭제했습니다.")
        return None

    def get_next(self):
        if self.last is None:
            print("리스트가 비어있습니다.")
            return None
        
        # current가 초기화되지 않은 경우
        if self.current is None:
            self.current = self.last.next
        else:
            self.current = self.current.next
        
        return self.current.data
    
    def search(self, keyword):
        if self.last is None:
            print("리스트가 비어있습니다.")
            return []
        
        results = []
        current = self.last.next
        index = 0
        
        # 원형 리스트를 한 바퀴 순회
        while True:
            if keyword.lower() in current.data.lower():
                results.append((index, current.data))
            
            current = current.next
            index += 1
            
            # 한 바퀴 돌아서 다시 첫 노드로 돌아온 경우
            if current == self.last.next:
                break
        
        if results:
            print(f"\n'{keyword}' 검색 결과: {len(results)}개 발견")
            for idx, data in results:
                print(f"  [{idx}] {data}")
        else:
            print(f"\n'{keyword}'에 대한 검색 결과가 없습니다.")
        
        return results

    def display(self):
        if self.last is None:
            print("플레이리스트가 비어있습니다.")
            return
        
        current = self.last.next
        print("\n=== 현재 원형 플레이리스트 ===")
        index = 0
        
        # 원형 리스트를 한 바퀴 순회
        while True:
            marker = " <- 현재 위치" if current == self.current else ""
            print(f"[{index}] {current.data}{marker}")
            current = current.next
            index += 1
            
            # 한 바퀴 돌아서 다시 첫 노드로 돌아온 경우
            if current == self.last.next:
                break
        
        print("(원형 리스트: 마지막 항목 다음은 다시 첫 항목)")
        print("=" * 40 + "\n")

def main():
    # 리스트 타입 선택
    print("=== 플레이리스트 타입 선택 ===")
    print("1. 링크드 리스트")
    print("2. 원형 순환 리스트")
    list_type = int(input("사용할 리스트 타입을 선택하세요: "))
    
    if list_type == 1:
        playlist = linkedlist()
        print("링크드 리스트를 선택하셨습니다.\n")
    elif list_type == 2:
        playlist = circularlist()
        print("원형 순환 리스트를 선택하셨습니다.\n")
    else:
        print("잘못된 선택입니다. 링크드 리스트로 시작합니다.")
        playlist = linkedlist()

    while True:
        print("1. 노드 추가")
        print("2. 노드 삭제")
        print("3. 노드 출력")
        if isinstance(playlist, circularlist):
            print("4. 다음 곡 재생")
            print("5. 음악 검색")
            print("6. 종료")
        else:
            print("4. 종료")
        choice = int(input("메뉴를 선택하세요: "))

        if choice == 1:
            print("1. 맨 앞에 추가")
            print("2. 맨 뒤에 추가")
            print("3. 중간에 추가")
            add_choice = int(input("메뉴를 선택하세요: "))
            if add_choice == 1:
                data = input("추가할 노드의 데이터를 입력하세요: ")
                playlist.insert(data, 0)
            elif add_choice == 2:
                data = input("추가할 노드의 데이터를 입력하세요: ")
                playlist.insert(data)
            elif add_choice == 3:
                data = input("추가할 노드의 데이터를 입력하세요: ")
                position = int(input("추가할 위치를 입력하세요: "))
                playlist.insert(data, position)
            else:
                print("잘못된 메뉴를 선택했습니다.")
        elif choice == 2:
            index = int(input("삭제할 노드의 인덱스를 입력하세요: "))
            playlist.delete(index)
        elif choice == 3:
            playlist.display()
        elif choice == 4:
            if isinstance(playlist, circularlist):
                next_song = playlist.get_next()
                if next_song:
                    print(f"다음 곡 재생: {next_song}")
            else:
                break
        elif choice == 5:
            if isinstance(playlist, circularlist):
                keyword = input("검색할 음악 제목을 입력하세요: ")
                playlist.search(keyword)
            else:
                print("잘못된 메뉴를 선택했습니다.")
        elif choice == 6:
            if isinstance(playlist, circularlist):
                break
            else:
                print("잘못된 메뉴를 선택했습니다.")
        else:
            print("잘못된 메뉴를 선택했습니다.")

if __name__ == "__main__":
    main()