import re
import math
import unicodedata


# Generate by ChatGPT 3.5
# Manually Modified
class Calculator:
    ans = 0.0  # 存储上一次计算的结果
    expression = ""  # 存储表达式

    def calc(self, expression: str):
        # 处理ANS关键字
        expression = unicodedata.normalize('NFKC', expression)
        self.expression = expression
        if "ANS" in expression:
            expression = expression.replace("ANS", str(self.ans))

        # 统计左括号和右括号数量
        left_count = expression.count('(')
        right_count = expression.count(')')

        # 自动补全右括号
        if left_count > right_count:
            expression += ')' * (left_count - right_count)

        # 处理log函数
        pattern = r'log\((\d+\.*\d*),(\d+\.*\d*)\)'
        while re.search(pattern, expression):
            match = re.search(pattern, expression)
            result = math.log(self.calc(match.group(2)),
                              self.calc(match.group(1)))
            expression = expression.replace(match.group(0), str(result))

        # 匹配括号
        pattern = r'\(([^()]+)\)'
        while re.search(pattern, expression):
            match = re.search(pattern, expression)
            result = self.calc(match.group(1))
            expression = expression.replace(match.group(0), str(result))

        # 处理乘除
        pattern = r'(\d+\.*\d*)([\*/])(\d+\.*\d*)'
        while re.search(pattern, expression):
            match = re.search(pattern, expression)
            if match.group(2) == '*':
                result = float(match.group(1)) * float(match.group(3))
            else:
                result = float(match.group(1)) / float(match.group(3))
            expression = expression.replace(match.group(0), str(result))

        # 处理加减
        pattern = r'(\d+\.*\d*)([\+\-])(\d+\.*\d*)'
        while re.search(pattern, expression):
            match = re.search(pattern, expression)
            if match.group(2) == '+':
                result = float(match.group(1)) + float(match.group(3))
            else:
                result = float(match.group(1)) - float(match.group(3))
            expression = expression.replace(match.group(0), str(result))

        # 存储结果和表达式
        self.ans = float(expression)

        # 返回结果
        return self.ans


# 测试代码
calculator = Calculator()
print(calculator.calc("1＋2"))
print(calculator.calc("2*ＡＮＳ"))
print(calculator.calc("log(10,ANS)"))
print(calculator.calc("3-ANS"))
print(calculator.expression)  # 输出上一次表达式
