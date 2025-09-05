import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt
import math

class Calculator:
    def __init__(self):
        self.expression = []
        self.current_num = ""
        self.just_calculated = False
        
        self.function_map = {
            'sin': self.calculate_sin,
            'cos': self.calculate_cos,
            'tan': self.calculate_tan,
            'sinh': self.calculate_sinh,
            'cosh': self.calculate_cosh,
            'tanh': self.calculate_tanh,
            'square': self.calculate_square,
            'cube': self.calculate_cube
        }

    def clear(self):
        self.expression = []
        self.current_num = ""
        self.just_calculated = False

    def add_number(self, number):
        self.current_num += number
        if self.just_calculated:
            self.expression = []
            self.just_calculated = False

    def add_decimal(self):
        if '.' not in self.current_num:
            if not self.current_num:
                self.current_num = "0."
            else:
                self.current_num += "."

    def commit_current_num(self):
        if self.current_num:
            self.expression.append(self.current_num)
            self.current_num = ""

    def add_operator(self, operator):
        if self.just_calculated:
            self.expression = []
            self.just_calculated = False
        
        self.commit_current_num()

        if self.expression and self.expression[-1] in "+-x÷":
            self.expression[-1] = operator
        else:
            self.expression.append(operator)

    def add_function(self, func_name):
        if self.just_calculated:
            self.expression = []
            self.just_calculated = False
        
        if self.current_num:
            func_expr = f"{func_name}({self.current_num})"
            self.expression.append(func_expr)
            self.current_num = ""
        elif self.expression and self.is_number_or_function(self.expression[-1]):
            last_val = self.expression.pop()
            func_expr = f"{func_name}({last_val})"
            self.expression.append(func_expr)

    def add_pi(self):
        if self.just_calculated:
            self.expression = []
            self.just_calculated = False
        
        if self.current_num:
            self.commit_current_num()
        
        self.expression.append('π')

    def is_number_or_function(self, token):
        if token in "+-x÷%":
            return False
        try:
            float(token)
            return True
        except ValueError:
            # 함수 형태인지 확인 (sin(30), square(5) 등)
            return '(' in token and ')' in token

    def percent(self):
        if self.just_calculated:
            self.expression = []
            self.just_calculated = False
        
        self.commit_current_num()
        if self.expression and self.expression[-1] not in "+-x÷%":
            self.expression.append('%')
        self.just_calculated = False

    def negative_positive(self):
        if self.just_calculated:
            self.expression = []
            self.just_calculated = False

        if self.current_num:
            try:
                val = float(self.current_num)
                self.current_num = str(-val)
            except ValueError:
                return
        else:
            return

    # 각 함수별 계산 메서드들
    def calculate_sin(self, value):
        num = float(value)
        result = math.sin(math.radians(num))
        return result

    def calculate_cos(self, value):
        num = float(value)
        result = math.cos(math.radians(num))
        return result

    def calculate_tan(self, value):
        num = float(value)
        if abs(math.cos(math.radians(num))) < 1e-10:
            raise ValueError("정의되지 않습니다")
        result = math.tan(math.radians(num))
        return result

    def calculate_sinh(self, value):
        num = float(value)
        result = math.sinh(num)
        return result

    def calculate_cosh(self, value):
        num = float(value)
        result = math.cosh(num)
        return result

    def calculate_tanh(self, value):
        num = float(value)
        result = math.tanh(num)
        return result

    def calculate_square(self, value):
        num = float(value)
        result = num ** 2
        return result

    def calculate_cube(self, value):
        num = float(value)
        result = num ** 3
        return result

    def parse_function_call(self, func_expr):
        open_paren = func_expr.find('(')
        close_paren = func_expr.find(')')
        
        if open_paren == -1 or close_paren == -1 or close_paren <= open_paren:
            return None, None
        
        func_name = func_expr[:open_paren]
        argument = func_expr[open_paren + 1:close_paren]
        
        return func_name, argument

    def evaluate_single_function(self, func_expr):
        func_name, argument = self.parse_function_call(func_expr)
        
        if func_name is None or argument is None:
            raise ValueError(f"잘못된 함수 형식: {func_expr}")
        
        if func_name not in self.function_map:
            raise ValueError(f"지원하지 않는 함수: {func_name}")
        try:
            argument_value = float(argument)
        except ValueError:
            return
        
        calculate_func = self.function_map[func_name]
        result = calculate_func(argument_value)
        
        return result

    def evaluate_functions_in_expression(self, expr_str):
        result_str = expr_str
        
        result_str = result_str.replace('π', str(math.pi))
        
        function_names = sorted(self.function_map.keys(), key=len, reverse=True)
        
        for func_name in function_names:
            pattern = f"{func_name}("
            
            while pattern in result_str:
                start_idx = result_str.find(pattern)
                
                if start_idx == -1:
                    break
                
                # 단순하게 첫 번째 ')' 찾기 (중첩 없으므로)
                open_paren = start_idx + len(func_name)
                close_paren = result_str.find(')', open_paren)
                
                if close_paren == -1:
                    raise ValueError(f"닫는 괄호를 찾을 수 없습니다: {func_name}")
                
                # 인수 추출 및 계산
                argument = result_str[open_paren + 1:close_paren]
                
                try:
                    arg_value = float(argument)
                    calc_result = self.function_map[func_name](arg_value)
                    
                    # 함수를 결과로 치환
                    result_str = result_str[:start_idx] + str(calc_result) + result_str[close_paren + 1:]
                    
                except ValueError:
                    raise ValueError(f"함수 인수는 숫자만 가능합니다: {argument}")
                except Exception as e:
                    raise ValueError(f"함수 계산 오류 ({func_name}({argument})): {e}")
        
        return result_str

    def calculate(self):
        self.commit_current_num()
        if not self.expression:
            return 0

        expr_str = "".join(self.expression)
        
        expr_str = self.evaluate_functions_in_expression(expr_str)
        
        expr_str = expr_str.replace('x', '*').replace('÷', '/').replace('%', '/100')

        try:
            result = eval(expr_str)
            
            # 결과 포맷팅
            if result == int(result):
                result_str = str(int(result))
            else:
                result_str = f"{result:.6f}".rstrip('0')
            
            self.expression = [result_str]
            self.current_num = result_str
            self.just_calculated = True
            return result
            
        except Exception as e:
            raise ValueError(f"계산 오류: {e}")

    def get_display_text(self):
        expr = self.expression.copy()
        if self.current_num:
            expr.append(self.current_num)
        if not expr:
            return "0"

        display_text = " ".join(expr)
        return display_text

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.btn_size = 60
        self.btn_space = 8
        self.start_x = 20
        self.start_y = 200
        self.calculator = Calculator()
        self.is_error = False
        self.initUI()

    def handle_error(self, error_msg):
        self.display.setText(error_msg)
        self.calculator.clear()
        self.is_error = True

    def update_display(self):
        if not self.is_error:
            if self.calculator.just_calculated:
                text = self.calculator.current_num
            else:
                text = self.calculator.get_display_text()
            self.display.setText(text)

    def number_btn_clicked(self):
        clicked = self.sender()
        number = clicked.text()
        if self.is_error:
            self.is_error = False
        self.calculator.add_number(number)
        self.update_display()

    def decimal_btn_clicked(self):
        if self.is_error:
            self.calculator.clear()
            self.is_error = False
        try:
            self.calculator.add_decimal()
            self.update_display()
        except Exception as e:
            self.handle_error(str(e))

    def operator_btn_clicked(self):
        if self.is_error:
            return
        clicked = self.sender()
        operator = clicked.text()
        try:
            self.calculator.add_operator(operator)
            self.update_display()
        except Exception as e:
            self.handle_error(str(e))

    def equals_btn_clicked(self):
        if self.is_error:
            return
        try:
            self.calculator.calculate()
            self.update_display()
        except Exception as e:
            self.handle_error(str(e))

    def function_btn_clicked(self):
        clicked = self.sender()
        function = clicked.text()

        if function == 'AC':
            self.calculator.clear()
            self.is_error = False
            self.update_display()
            
        elif function == '+/-':
            if self.is_error:
                return
            self.calculator.negative_positive()
            self.update_display()
            
        elif function == '%':
            if self.is_error:
                return
            try:
                self.calculator.percent()
                self.update_display()
            except Exception as e:
                self.handle_error(str(e))
                
        elif function in ['sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh']:
            try:
                self.calculator.add_function(function)
                self.update_display()
            except Exception as e:
                self.handle_error(str(e))
                
        elif function == 'x²':
            try:
                self.calculator.add_function('square')
                self.update_display()
            except Exception as e:
                self.handle_error(str(e))
                
        elif function == 'x³':
            try:
                self.calculator.add_function('cube')
                self.update_display()
            except Exception as e:
                self.handle_error(str(e))
                
        elif function == 'π':
            try:
                self.calculator.add_pi()
                self.update_display()
            except Exception as e:
                self.handle_error(str(e))

    def get_button_position(self, row, col):
        x = self.start_x + col * (self.btn_size + self.btn_space)
        y = self.start_y + row * (self.btn_size + self.btn_space)
        return x, y

    def create_button(self, text, row, col, button_type, width=1):
        x, y = self.get_button_position(row, col)
        btn_width = self.btn_size * width + self.btn_space * (width - 1)
        btn = QPushButton(text, self)
        btn.setGeometry(x, y, btn_width, self.btn_size)
        
        # 스타일 설정
        if button_type == 'number':
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
        
        # 이벤트 연결
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

    def initUI(self):
        """공학용 계산기 UI 초기화"""
        self.setWindowTitle('Engineering Calculator')
        self.setGeometry(100, 100, 700, 552)
        self.setStyleSheet("background-color: black;")

        # 디스플레이
        self.display = QLabel('0', self)
        self.display.setGeometry(20, 50, 660, 80)
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

        # 버튼 배치 (기존과 동일)
        # 첫 번째 줄
        self.create_button('(', 0, 0, 'function')
        self.create_button(')', 0, 1, 'function')
        self.create_button('mc', 0, 2, 'function')
        self.create_button('m+', 0, 3, 'function')
        self.create_button('m-', 0, 4, 'function')
        self.create_button('mr', 0, 5, 'function')
        self.create_button('AC', 0, 6, 'function')
        self.create_button('+/-', 0, 7, 'function')
        self.create_button('%', 0, 8, 'function')
        self.create_button('÷', 0, 9, 'operator')

        # 두 번째 줄
        self.create_button('2ⁿᵈ', 1, 0, 'function')
        self.create_button('x²', 1, 1, 'function')
        self.create_button('x³', 1, 2, 'function')
        self.create_button('xʸ', 1, 3, 'function')
        self.create_button('eˣ', 1, 4, 'function')
        self.create_button('10ˣ', 1, 5, 'function')
        self.create_button('7', 1, 6, 'number')
        self.create_button('8', 1, 7, 'number')
        self.create_button('9', 1, 8, 'number')
        self.create_button('x', 1, 9, 'operator')

        # 세 번째 줄
        self.create_button('¹⁄ₓ', 2, 0, 'function')
        self.create_button('²√x', 2, 1, 'function')
        self.create_button('³√x', 2, 2, 'function')
        self.create_button('ʸ√x', 2, 3, 'function')
        self.create_button('ln', 2, 4, 'function')
        self.create_button('log', 2, 5, 'function')
        self.create_button('4', 2, 6, 'number')
        self.create_button('5', 2, 7, 'number')
        self.create_button('6', 2, 8, 'number')
        self.create_button('-', 2, 9, 'operator')

        # 네 번째 줄
        self.create_button('x!', 3, 0, 'function')
        self.create_button('sin', 3, 1, 'function')
        self.create_button('cos', 3, 2, 'function')
        self.create_button('tan', 3, 3, 'function')
        self.create_button('e', 3, 4, 'function')
        self.create_button('EE', 3, 5, 'function')
        self.create_button('1', 3, 6, 'number')
        self.create_button('2', 3, 7, 'number')
        self.create_button('3', 3, 8, 'number')
        self.create_button('+', 3, 9, 'operator')

        # 다섯 번째 줄
        self.create_button('Rad', 4, 0, 'function')
        self.create_button('sinh', 4, 1, 'function')
        self.create_button('cosh', 4, 2, 'function')
        self.create_button('tanh', 4, 3, 'function')
        self.create_button('π', 4, 4, 'function')
        self.create_button('Rand', 4, 5, 'function')
        self.create_button('0', 4, 6, 'number', width=2)
        self.create_button('.', 4, 8, 'number')
        self.create_button('=', 4, 9, 'operator')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
