import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt


class Calculator:
    def __init__(self):
        self.expression = []
        self.current_num = ''
        self.just_calculated = False

    def clear(self):
        self.expression = []
        self.current_num = ''
        self.just_calculated = False

    def add_number(self, number):
        self.current_num += number
        if self.just_calculated:
            self.expression = []
            self.just_calculated = False

    def add_decimal(self):
        if '.' not in self.current_num:
            if not self.current_num:
                self.current_num = '0.'
            else:
                self.current_num += '.'

    def commit_current_num(self):
        if self.current_num:
            self.expression.append(self.current_num)
            self.current_num = ''

    def add_operator(self, operator):
        if self.just_calculated:
            self.expression = []
            self.just_calculated = False

        self.commit_current_num()

        if self.expression and self.expression[-1] in '+-x÷':
            self.expression[-1] = operator
        else:
            self.expression.append(operator)

    def percent(self):
        if self.just_calculated:
            self.expression = []
            self.just_calculated = False

        self.commit_current_num()

        if self.expression and self.expression[-1] not in '+-x÷%':
            self.expression.append('%')
        else:
            return
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

        self.just_calculated = False

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError('0으로 나눌 수 없습니다')
        return a / b

    def change_percent(self, expr):
        result = ''
        i = 0
        length = len(expr)

        while i < length:
            if expr[i] == '%':
                # % 다음에 오는 것이 무엇인지 확인
                if i + 1 < length:
                    # 공백을 건너뛰고 다음 유효한 문자 찾기
                    j = i + 1
                    while j < length and expr[j] == ' ':
                        j += 1

                    if j < length:
                        next_char = expr[j]
                        # 다음 문자가 숫자면 모듈러 연산 (% 그대로 유지)
                        if next_char.isdigit():
                            result += '%'
                        # 다음 문자가 연산자면 백분율 (/100으로 변환)
                        elif next_char in '+-*/':
                            result += '/100'
                        else:
                            result += '%'  # 기본값
                    else:
                        result += '/100'  # 마지막에 %가 오면 백분율
                else:
                    result += '/100'  # 마지막에 %가 오면 백분율
            else:
                result += expr[i]
            i += 1

        return result

    def equal(self):
        self.commit_current_num()
        if not self.expression:
            return 0

        # 연산자 개수 확인을 위해 expression을 분석
        operators = [token for token in self.expression if token in '+-x÷']

        # 연산자가 1개인 경우 메서드 사용
        if len(operators) == 1 and '%' not in self.expression:
            try:
                # 숫자와 연산자 분리
                numbers = [
                    token for token in self.expression if token not in '+-x÷%'
                ]
                operator = operators[0]

                if len(numbers) >= 2:
                    a = float(numbers[0])
                    b = float(numbers[1])

                    # 연산자에 따라 메서드 호출
                    if operator == '+':
                        result = self.add(a, b)
                    elif operator == '-':
                        result = self.subtract(a, b)
                    elif operator == 'x':
                        result = self.multiply(a, b)
                    elif operator == '÷':
                        result = self.divide(a, b)
                    else:
                        raise ValueError('알 수 없는 연산자')
                else:
                    return

            except Exception as e:
                raise ValueError(f'계산 오류: {e}')

        else:
            expr = ' '.join(self.expression)
            expr = self.change_percent(expr)
            expr = expr.replace('x', '*').replace('÷', '/')
            try:
                result = eval(expr)
            except Exception as e:
                raise ValueError(f'계산 오류: {e}')

        # 결과 포맷팅
        if result == int(result):
            result_str = str(int(result))
        else:
            result_str = f'{result:.6f}'.rstrip('0')

        self.expression = [result_str]
        self.current_num = result_str
        self.just_calculated = True
        return result

    def get_display_text(self):
        expr = self.expression.copy()
        if self.current_num:
            expr.append(self.current_num)
        if not expr:
            return '0'

        display_text = ' '.join(expr)
        return display_text


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.btn_size = 80
        self.btn_space = 10
        self.start_x = 20
        self.start_y = 200
        self.calculator = Calculator()
        self.is_error = False
        self.initUI()

    def handle_error(self, error_msg):
        print(error_msg)
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
            self.calculator.equal()
            self.update_display()
        except Exception as e:
            self.handle_error(str(e))

    def function_btn_clicked(self):
        clicked = self.sender()
        function = clicked.text()

        if function == 'C':
            self.calculator.clear()
            self.is_error = False
            self.update_display()

        elif function == '%':
            if self.is_error:
                return

            try:
                self.calculator.percent()
                self.update_display()
            except Exception as e:
                self.handle_error(str(e))

        elif function == '+/-':
            if self.is_error:
                return

            self.calculator.negative_positive()
            self.update_display()

    def get_button_position(self, row, col):
        x = self.start_x + col * (self.btn_size + self.btn_space)
        y = self.start_y + row * (self.btn_size + self.btn_space)
        return x, y

    def create_button(self, text, row, col, button_type, width=1):
        x, y = self.get_button_position(row, col)
        btn_width = self.btn_size * width + self.btn_space * (width - 1)
        btn = QPushButton(text, self)
        btn.setGeometry(x, y, btn_width, self.btn_size)

        if button_type == 'number':
            style = """
                QPushButton {
                    border-radius: 40px;
                    background-color: #565656;
                    color: white;
                    font-size: 24px;
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
                    border-radius: 40px;
                    background-color: #f19b38;
                    color: white;
                    font-size: 24px;
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
                    border-radius: 40px;
                    background-color: #8e8e92;
                    color: black;
                    font-size: 20px;
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
        self.setWindowTitle('My Calculator')
        self.setGeometry(100, 100, 400, 660)
        self.setStyleSheet('background-color: black;')

        self.display = QLabel('0', self)
        self.display.setGeometry(20, 50, 350, 100)
        self.display.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 48px;
                font-weight: 300;
                background-color: black;
                border: none;
                padding-right: 20px;
            }
        """)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.btn_clear = self.create_button('C', 0, 0, 'function')
        self.btn_plus_minus = self.create_button('+/-', 0, 1, 'function')
        self.btn_percent = self.create_button('%', 0, 2, 'function')
        self.btn_divide = self.create_button('÷', 0, 3, 'operator')

        self.btn_7 = self.create_button('7', 1, 0, 'number')
        self.btn_8 = self.create_button('8', 1, 1, 'number')
        self.btn_9 = self.create_button('9', 1, 2, 'number')
        self.btn_multiply = self.create_button('x', 1, 3, 'operator')

        self.btn_4 = self.create_button('4', 2, 0, 'number')
        self.btn_5 = self.create_button('5', 2, 1, 'number')
        self.btn_6 = self.create_button('6', 2, 2, 'number')
        self.btn_minus = self.create_button('-', 2, 3, 'operator')

        self.btn_1 = self.create_button('1', 3, 0, 'number')
        self.btn_2 = self.create_button('2', 3, 1, 'number')
        self.btn_3 = self.create_button('3', 3, 2, 'number')
        self.btn_plus = self.create_button('+', 3, 3, 'operator')

        self.btn_0 = self.create_button('0', 4, 0, 'number', width=2)
        self.btn_dot = self.create_button('.', 4, 2, 'number')
        self.btn_equals = self.create_button('=', 4, 3, 'operator')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
