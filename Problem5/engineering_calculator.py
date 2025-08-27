import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.btn_size = 60      # 버튼 크기
        self.btn_space = 8     # 버튼 간격
        self.start_x = 20      
        self.start_y = 200
        self.calculator = Calculator()
        self.expr = ""
        self.current_num = '0'
        self.has_decimal_point = False
        self.is_error = False
        self.initUI()

    def get_button_position(self, row, col):
        x = self.start_x + col * (self.btn_size + self.btn_space)
        y = self.start_y + row * (self.btn_size + self.btn_space)
        return x, y

    def create_button(self, text, row, col, button_type , width = 1):
        x, y = self.get_button_position(row, col)

        btn_width = self.btn_size * width + self.btn_space * (width - 1)

        btn = QPushButton(text, self)
        btn.setGeometry(x, y, btn_width, self.btn_size)

        if button_type == 'number':
            # 회색 숫자 버튼
            style = """
                QPushButton {
                    border-radius: 30px;
                    background-color: #565656;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:pressed {
                    background-color: #000000;
                }
            """
        elif button_type == 'operator':
            # 주황색 연산자 버튼
            style = """
                QPushButton {
                    border-radius: 30px;
                    background-color: #f19b38;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:pressed {
                    background-color: #000000;
                }
            """
        elif button_type == 'function':
            # 연회색 기능 버튼
            style = """
                QPushButton {
                    border-radius: 30px;
                    background-color: #8e8e92;
                    color: black;
                    font-size: 12px;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:pressed {
                    background-color: #575763;
                }
            """
        
        btn.setStyleSheet(style)

        if button_type == 'number':
            if text == '.':
                btn.clicked.connect(self.decimal_btn_clicked)
            else:
                btn.clicked.connect(self.number_btn_clicked)
        elif button_type == 'operator':
            if text == '=':
                btn.clicked.connect(self.equals_btn_clicked)
            else:
                btn.clicked.connect(self.operator_btn_clicked)
        elif button_type == 'function':
            btn.clicked.connect(self.function_btn_clicked)
        
        return btn
    
    def number_btn_clicked(self):
        clicked = self.sender() # 클릭된 버튼 객체
        number = clicked.text()

        if self.is_error:
            self.current_num = number
            self.display.setText(number)
            self.calculator.reset()
            self.has_decimal_point = False
            self.is_error = False
            return

        if len(self.current_num.replace('.', '')) >= 10:
            return  # 더 이상 입력 받지 않음
        
        # 현재 화면이 "0"이면 새로운 숫자로 교체
        if self.current_num == '0' or self.calculator.waiting:
            self.current_num = number
            if self.calculator.waiting:
                self.expr += f" {number}"  # 연산자 뒤에 숫자 추가
            else:
                self.expr = number  # 처음 시작
            self.calculator.waiting = False
            self.display.setText(number)
            self.has_decimal_point = False
            self.calculator.waiting = False
        else:
            # 기존 숫자 뒤에 새로운 숫자 추가
            self.current_num += number
            if ' ' in self.expr:
                # 수식이 있으면 마지막 숫자만 교체
                parts = self.expr.split()
                parts[-1] = self.current_num
                self.expr = ' '.join(parts)
            else:
                # 수식이 없으면 그냥 추가
                self.expr = self.current_num

        self.display.setText(self.expr)
        self.has_decimal_point = False
    
    def decimal_btn_clicked(self):
        if self.has_decimal_point or self.is_error:
            return
    
        if self.calculator.waiting:
            self.current_num = "0."
            self.expr += " 0."
            self.calculator.waiting = False
        else:
            self.current_num += "."
            if ' ' in self.expr:
                parts = self.expr.split()
                parts[-1] = self.current_num
                self.expr = ' '.join(parts)
            else:
                self.expr = self.current_num
        self.display.setText(self.expr)
        self.has_decimal_point = True

    def operator_btn_clicked(self):
        clicked_btn = self.sender()
        operator = clicked_btn.text()

        if self.is_error:
            return

        try:
            # ✅ 연속 연산자 입력 시 마지막 연산자만 교체
            if self.calculator.waiting:
                parts = self.expr.split()
                parts[-1] = operator  # 마지막 연산자 교체
                self.expr = ' '.join(parts)
            else:
                # ✅ 새 연산자 추가
                self.expr += f" {operator}"
            self.calculator.set_operator(operator, self.current_num)
            self.display.setText(self.expr)
            self.has_decimal_point = False
        except ValueError as e:
            self.display.setText("Error")
            print(f"연산자 입력 오류: {e}")

    def function_btn_clicked(self):
        clicked_btn = self.sender()
        function = clicked_btn.text()

        try:
            if function != 'AC' and self.is_error:
                return

            if function == 'AC':
                self.display.setText('0')
                self.expr = ''
                self.current_num = '0'  
                self.calculator.reset()
                self.has_decimal_point = False
                self.is_error = False

            elif function == '+/-':
                result = self.calculator.negative_positive(self.current_num)
                if result == int(result):
                    result_text = str(int(result))
                else:
                    result_text = f"{result:.6g}"
                
                # ✅ current_num과 수식 모두 업데이트
                self.current_num = result_text
                if ' ' in self.expr:
                    parts = self.expr.split()
                    parts[-1] = result_text
                    self.expr = ' '.join(parts)
                else:
                    self.expr = result_text
                    
                self.display.setText(self.expr)
                self.has_decimal_point = '.' in result_text
                
            elif function == '%':
                    # ✅ % 버튼을 연산자처럼 처리
                if self.calculator.waiting:
                    # 연속 % 입력 시 마지막 연산자 교체
                    parts = self.expr.split()
                    parts[-1] = '%'
                    self.expr = ' '.join(parts)
                else:
                    # 새 % 연산자 추가
                    self.expr += ' %'
                
                self.calculator.set_operator('%', self.current_num)
                self.display.setText(self.expr)
                self.has_decimal_point = False
                
        except ValueError as e:
            self.display.setText("Error")
            self.is_error = True
            print(f"기능 버튼 오류: {e}")

    def equals_btn_clicked(self):
        if self.is_error:
            return

        try:
        # ✅ % 연산자가 포함된 경우 특별 처리
            if '%' in self.expr:
                parts = self.expr.split()
                if len(parts) == 2 and parts[1] == '%':
                    # "숫자 %" 형태면 백분율 계산
                    result = self.calculator.percent(parts[0])
                else:
                    # 복잡한 수식이면 일반 계산
                    result = self.calculator.equal(self.current_num)
            else:
                result = self.calculator.equal(self.current_num)
            
            if result == int(result):
                result_text = str(int(result))
            else:
                result_text = f"{result:.6g}"
            
            self.display.setText(result_text)
            self.expr = result_text
            self.current_num = result_text
            self.has_decimal_point = '.' in result_text
        except ValueError as e:
            self.display.setText(f"{e}")
            self.calculator.reset()
            self.current_num = "0" 
            self.expr = ""
            self.has_decimal_point = False
            self.is_error = True
            print(f"{e}")

    def extract_last_number(self):
        if not self.expr:
            return "0"
        
        parts = self.expr.split()
        if parts and parts[-1] not in ['+', '-', 'x', '÷']:
            return parts[-1]
        
        # 연산자로 끝나면 그 앞의 숫자 반환
        if len(parts) >= 2:
            return parts[-2]
        
        return "0"

    def replace_last_number(self, new_number):
        """수식에서 마지막 숫자를 새로운 값으로 교체하는 메서드"""
        if not self.expr:
            self.expr = new_number
            return
        
        parts = self.expr.split()
        if parts and parts[-1] not in ['+', '-', 'x', '÷']:
            # 마지막이 숫자면 교체
            parts[-1] = new_number
            self.expr = ' '.join(parts)
        else:
            # 마지막이 연산자면 숫자 추가
            self.expr += new_number

    def initUI(self):
        self.setWindowTitle('My calculator')
        self.setGeometry(100, 100, 700, 552)
        self.setStyleSheet("background-color: black;")

        # 맨 위 출력
        self.display = QLabel('0', self)
        self.display.setGeometry(20, 60, 680, 40)
        self.display.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 36px;
                font-weight: 300;
                background-color: black;
                border: none;
                padding-right: 20px;
            }
        """)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # ✅ 첫 번째 줄 - 괄호 및 메모리 기능
        self.btn_open_paren = self.create_button('(', 0, 0, 'function')
        self.btn_close_paren = self.create_button(')', 0, 1, 'function')
        self.btn_mc = self.create_button('mc', 0, 2, 'function')
        self.btn_m_plus = self.create_button('m+', 0, 3, 'function')
        self.btn_m_minus = self.create_button('m-', 0, 4, 'function')
        self.btn_mr = self.create_button('mr', 0, 5, 'function')
        self.btn_ac = self.create_button('AC', 0, 6, 'function')
        self.btn_plus_minus = self.create_button('+/-', 0, 7, 'function')
        self.btn_percent = self.create_button('%', 0, 8, 'function')
        self.btn_divide = self.create_button('÷', 0, 9, 'operator')

        # ✅ 두 번째 줄 - 지수, 거듭제곱 함수
        self.btn_2nd = self.create_button('2ⁿᵈ', 1, 0, 'function')
        self.btn_x_squared = self.create_button('x²', 1, 1, 'function')
        self.btn_x_cubed = self.create_button('x³', 1, 2, 'function')
        self.btn_x_power_y = self.create_button('xʸ', 1, 3, 'function')
        self.btn_e_power_x = self.create_button('eˣ', 1, 4, 'function')  # ✅ e^x로 수정
        self.btn_10_power_x = self.create_button('10ˣ', 1, 5, 'function')  # ✅ 10^x로 수정
        self.btn_7 = self.create_button('7', 1, 6, 'number')
        self.btn_8 = self.create_button('8', 1, 7, 'number')
        self.btn_9 = self.create_button('9', 1, 8, 'number')
        self.btn_multiply = self.create_button('x', 1, 9, 'operator')

        # ✅ 세 번째 줄 - 역함수, 루트 함수
        self.btn_1_over_x = self.create_button('¹⁄ₓ', 2, 0, 'function')
        self.btn_sqrt = self.create_button('²√x', 2, 1, 'function')
        self.btn_cube_root = self.create_button('³√x', 2, 2, 'function')
        self.btn_y_root_x = self.create_button('ʸ√x', 2, 3, 'function')
        self.btn_ln = self.create_button('ln', 2, 4, 'function')  # ✅ 자연로그 ln으로 수정
        self.btn_log10 = self.create_button('log', 2, 5, 'function')  # ✅ 상용로그 log (log10)으로 수정
        self.btn_4 = self.create_button('4', 2, 6, 'number')
        self.btn_5 = self.create_button('5', 2, 7, 'number')
        self.btn_6 = self.create_button('6', 2, 8, 'number')
        self.btn_minus = self.create_button('-', 2, 9, 'operator')

        # ✅ 네 번째 줄 - 팩토리얼, 삼각함수
        self.btn_factorial = self.create_button('x!', 3, 0, 'function')
        self.btn_sin_inv = self.create_button('sin⁻¹', 3, 1, 'function')
        self.btn_cos_inv = self.create_button('cos⁻¹', 3, 2, 'function')
        self.btn_tan_inv = self.create_button('tan⁻¹', 3, 3, 'function')
        self.btn_e = self.create_button('e', 3, 4, 'function')
        self.btn_ee = self.create_button('EE', 3, 5, 'function')
        self.btn_1 = self.create_button('1', 3, 6, 'number')
        self.btn_2 = self.create_button('2', 3, 7, 'number')
        self.btn_3 = self.create_button('3', 3, 8, 'number')
        self.btn_plus = self.create_button('+', 3, 9, 'operator')

        # 다섯 번째 줄 (0, ., =)
        self.btn_calculator_icon = self.create_button('o', 4, 0, 'function')  # 계산기 아이콘
        self.btn_sinh_inv = self.create_button('sinh⁻¹', 4, 1, 'function')
        self.btn_cosh_inv = self.create_button('cosh⁻¹', 4, 2, 'function')
        self.btn_tanh_inv = self.create_button('tanh⁻¹', 4, 3, 'function')
        self.btn_pi = self.create_button('π', 4, 4, 'function')
        self.btn_rad = self.create_button('Rad', 4, 5, 'function')
        self.btn_rand = self.create_button('Rand', 4, 6, 'function')
        self.btn_0 = self.create_button('0', 4, 7, 'number')
        self.btn_dot = self.create_button('.', 4, 8, 'number')
        self.btn_equals = self.create_button('=', 4, 9, 'operator')


class Calculator:
    MAX_VALUE = 999999999

    def __init__(self):
        self.result = 0.0
        self.current_input = ""
        self.operator = ""
        self.waiting = False
    
    def check_max(self, val):
        """결과값 검증"""
        if abs(val) > self.MAX_VALUE:
            raise ValueError("결과가 너무 크다")
        return val


    def add(self, a, b):
        try:
            result = float(a) + float(b)
            return self.check_max(result)
        except (ValueError, TypeError) as e:
            raise ValueError(f"덧셈 연산 오류: {e}")
    
    def subtract(self, a, b):
        try:
            result = float(a) - float(b)
            return self.check_max(result)
        except (ValueError, TypeError) as e:
            raise ValueError(f"뺄셈 연산 오류: {e}")
    
    def multiply(self, a, b):
        try:
            result = float(a) * float(b)
            return self.check_max(result)
        except (ValueError, TypeError) as e:
            raise ValueError(f"곱셈 연산 오류: {e}")
    
    def divide(self, a, b):
        try:
            divisor = float(b)
            if divisor == 0:
                raise ValueError("정의되지 않은 값")
            
            result = float(a) / divisor
            return self.check_max(result)
        except (ValueError, TypeError) as e:
            raise ValueError(f"나눗셈 연산 오류: {e}")
        
    def reset(self):
        self.result = 0.0
        self.current_input = ""
        self.operator = ""
        self.waiting = False
    
    def negative_positive(self, value):
        try:
            number = float(value)
            result = -number  
            return self.check_max(result)
        except (ValueError, TypeError) as e:
            raise ValueError(f"부호 변환 오류: 숫자가 아닌 값입니다 - {e}")
        
    def percent(self, value):
        try:
            number = float(value)
            result = number / 100.0
            return self.check_max(result)
        except (ValueError, TypeError) as e:
            raise ValueError(f"백분율 계산 오류: 숫자가 아닌 값입니다 - {e}")
    
    def equal(self, result_val):
        try:
            if not self.operator:
                # 연산자가 없으면 현재 입력값을 그대로 반환
                return float(result_val)
            
            second_operand = float(result_val)
            
            # 연산자에 따라 해당 메서드 호출
            if self.operator == '+':
                result = self.add(self.result, second_operand)
            elif self.operator == '-':
                result = self.subtract(self.result, second_operand)
            elif self.operator == 'x':
                result = self.multiply(self.result, second_operand)
            elif self.operator == '/' or self.operator == '÷':
                result = self.divide(self.result, second_operand)
            else:
                raise ValueError(f"알 수 없는 연산자: {self.operator}")
            
            # 계산 완료 후 상태 초기화
            self.result = 0.0
            self.operator = ""
            self.waiting = False
            
            return result
            
        except Exception as e:
            # 오류 발생 시 초기화하고 오류 메시지 반환
            self.reset()
            raise ValueError(f"계산 오류: {e}")
        
    def set_operator(self, operator, current_num):
        try:
            self.result = float(current_num)
            self.operator = operator
            self.waiting = True
        except (ValueError, TypeError) as e:
            raise ValueError(f"연산자 설정 오류: {e}")

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   ex.show()
   sys.exit(app.exec_())