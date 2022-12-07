# encoding=utf-8
'''
Filename : 累加器.py
Datatime : 2022/12/07 
Author :KJH-x
'''


from traceback import print_exc
import math


def output(result: ...) -> None:
    if type(result) == "<class 'str'>":
        print(f"==> {result}")
    else:
        # print("---Long Result:---start---")
        print(result)
        # print("---Long Result:--- end ---")
    history.append(result)


def isfloat(expression: str) -> bool:
    if expression.count(".") < 2:
        return expression.replace(".", "").isdigit()
    else:
        return False


def isfunction(expression: str) -> bool:
    for br in bracket:
        expression = expression.replace(br, "")
    return expression.isalpha()


def assign_class(operator) -> list:
    for i in range(len(level)):
        if operator in level[i]:
            return [operator, i]
    print(f"Unreachable!,with input={operator}")
    raise ValueError


def flash(command='part') -> None:
    global Ans, last, history
    if command in ['part', 'full']:
        Ans = 0
        last = 0
        if command == 'full':
            history = []


def convert(expression: str) -> list:
    cache = []
    left = right = 0
    bracketlevel = 0
    # 输入为空，直接下一轮
    if expression == "":
        output("")
        return []
    # 输入查询记录
    elif expression.lower() in ['memory', 'mem']:
        print(memory)
    # 输入分析：
    while left < len(expression):
        append = ""
        print(f"==interval left={left} right={right}")
        if expression[left].isdigit():
            # 触发过程量记录
            for right in range(left+1, len(expression)+1):

                if isfloat(expression[left:right]):
                    append = float(expression[left:right])
                else:
                    right -= 1
                    break
            cache.append(append)
            last_type = "number"
            left = right
            continue

        elif expression[left] in rightclass:
            if expression[left] == '!':
                # 阶乘立刻计算
                cache.append(math.factorial(cache.pop()))
            last_type = "number"
            left += 1
            continue

        elif expression[left] in midclass:
            # 记录二元运算符
            # 二元运算符应等待其后的运算结果
            cache.append(assign_class(expression[left]))
            last_type = "operator"
            left += 1
            continue

        elif expression[left].isalpha():
            # 记录函数
            for right in range(left+1, len(expression)+1):
                if isfunction(expression[left:right]):
                    append = [expression[left:right], bracketlevel]
                else:
                    right -= 1
                    break
            cache.append(append)
            last_type = "function"
            left = right
            bracketlevel += 1
            continue

        elif expression[left] in Lbracket:
            cache.append([str(expression)[left], bracketlevel])
            left += 1
            bracketlevel += 1
            continue

        elif expression[left] in Rbracket:
            bracketlevel -= 1
            cache.append([str(expression)[left], bracketlevel])
            left += 1
            continue

        elif expression[left] in [",", "，"]:
            left += 1
            continue
    if bracketlevel != 0:
        print("bracket not close!")
    return cache


def calculate(cache: list) -> float:
    # working
    return 0


def solve(cache: list) -> float:
    # schedule
    return 0


midclass = ['+', '-', '*', '/', '%', '^', 'A', 'P', 'C',]
rightclass = ['!']
Lbracket = ['(', '[', '{', '（', '【']
Rbracket = [')', ']', '}', '）',  '】']

level = [
    ["nothing"],
    ["+", "-"],
    ["*", "/", "%"],
    ["^"],
    ["A", "P", "C"],
    ['(', ')', '[', ']', '{', '}', '（', '）', '【', '】']
]
Ans = 0
last = 0
history = []
if __name__ == '__main__':

    memory = []
    last_type = ""
    flash()
    while True:
        try:
            # 输入，去除空格和前后空白符
            expression = input().strip().replace(" ", "")
            cache = convert(expression)
            print("==>cache:")
            output(cache)
            if expression.count("=") == 0:
                calculate(cache)
            else:
                solve(cache)

        except EOFError:
            Ans = history.pop()
            print(f"==Undo==> Ans = {Ans}")
        except KeyboardInterrupt:
            exit()
        except Exception:
            print_exc()
            input()
