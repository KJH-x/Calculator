# encoding=utf-8
# python_version>=3.10
'''
Filename : 累加器.py
Datatime : 2022/12/07
Author :KJH-x
'''


import math
import sys
import re
import copy


class ExpressionError(SyntaxError):
    """Wrong Input Syntax
    """

    def __init__(self, msg: str,):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
    pass


class UnreachableError(SyntaxError):
    """Branch that should not be reached
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
    pass


def ShowStep(content: list):
    """Show calculate step

    Args:
        content (list): cache sequence
    """
    isolateContent = copy.deepcopy(content)
    for x in range(len(isolateContent)):
        if isinstance(isolateContent[x], list):
            isolateContent[x] = str(isolateContent[x][0])
        else:
            pass
    # isolateContent = re.sub(".0", '', f"{isolateContent}")
    isolateContent = re.sub(
        "[\\[\\]\\,\\'\\s]", '',
        f"{isolateContent}".replace(".0", "")
    ).replace(";", ",")
    print(f'\t{isolateContent}')
    return


def output(result: ...) -> None:
    """[Deprecated] Print someting formatted

    Args:
        result (str or any): things to print
    """
    # 此函数功能目前不佳，在好的替代方案发现之前
    # 新增的输出内容，直接用print
    if type(result) == "<class 'str'>":
        print(f"==> {result}")
    else:
        # print("---Long Result:---start---")
        print(result)
        # print("---Long Result:--- end ---")
    history.append(result)


def ParameterCounter(sequence: list) -> int:
    """Count the parameter in sequence by counting comma

    Args:
        sequence (list): sequence to count

    Returns:
        int: number of parameter(s) but not comma
    """
    count = 1
    for i in sequence:
        if i == ';':
            count += 1
    return count


def isfloat(expression: str) -> bool:
    """Judge if the expression is an acceptble float number
    """
    if expression.count('.') < 2 and expression.count('e') < 2:
        return expression.replace(".", "").isdigit()
    else:
        return False


def iscomplex(expression: str) -> bool:
    """Judge if the expression is an acceptble complex number
    """
    # new
    return False


def isfunction(expression: str) -> bool:
    """Judge if the expression is an acceptble function
    """
    expression = re.sub('[(]', "", expression)
    return expression.isalpha()


def assign_class(operator) -> list:
    """assign class for opertor

    Raises:
        UnreachableError: opertor not support

    Returns:
        list: [opertor, class]
    """
    for i in range(len(level)):
        if operator in level[i]:
            return [operator, i]
    raise UnreachableError(
        f"Unknown opertor: {operator}"
    )


def flash(command='part') -> None:
    global Ans, last, history
    if command in ['part', 'full']:
        Ans = 0
        last = 0
        if command == 'full':
            history = []


def convert(expression: str) -> list:
    """Convert the input to comprehensive structure

    Args:
        expression (str): input string

    Returns:
        list: cache: made up of floats operator and function
    """
    cache = []
    left, right = [0, 0]
    # 括号优先级计算，左括号加一级，右括号减一级
    # 输入的括号可不在形式上成对，只要左右个数一致即可
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
        function = ""
        if expression[left].isdigit():
            # 过程量记录
            # 调用isfloat函数，把小数吃掉
            for right in range(left+1, len(expression)+1):

                if isfloat(expression[left:right]):
                    function = float(expression[left:right])
                else:
                    right -= 1
                    break
            cache.append(function)
            # last_type = "number"
            left = right
            continue

        elif expression[left] in rightclass:
            if expression[left] == '!':
                # 阶乘立刻计算
                # 后续可能需要改进，这将导致能约分的出现故障
                # 似乎不应该立刻计算，再考虑一下
                cache.append(math.factorial(int(cache.pop())))
            # last_type = "number"
            left += 1
            continue

        elif expression[left] in midclass:
            # 记录二元运算符
            # 二元运算符应等待其后的运算结果
            cache.append(assign_class(expression[left]))
            # last_type = "operator"
            left += 1
            continue

        elif expression[left].isalpha():
            # 记录函数
            # 调用isfunction来把一串英文和后随括号给吃掉
            for right in range(left+1, len(expression)+1):
                if isfunction(expression[left:right]):
                    function = [expression[left:right], bracketlevel]
                else:
                    right -= 1
                    break
            if function[0][-1] != '(':
                print(
                    f"\n[Warn] Skipping incomprehensible '{function[0]}'")
                left += 1
            else:
                # 如果前面一个是数字，那么是缩写，把没有的乘号补上
                if len(cache) > 0 and isinstance(cache[-1], float):
                    cache.append(assign_class('*'))
                # 记录的时候记录函数名称
                cache.append(function)
                # last_type = function
                left = right
                bracketlevel += 1
            continue

        elif expression[left] == '(':
            # 如果前一个是数字，那么是缩写，把没有的乘号补上
            if len(cache) > 0 and isinstance(cache[-1], float):
                cache.append(assign_class('*'))
            # 遇到左侧等号，处理后加一级
            cache.append([str(expression)[left], bracketlevel])
            left += 1
            bracketlevel += 1
            continue

        elif expression[left] == ')':
            # 遇到右侧等号，处理前减一级
            bracketlevel -= 1
            cache.append([str(expression)[left], bracketlevel])
            left += 1
            continue

        elif expression[left] == ';':
            # 多个参数不好处理，由拆分函数执行任务分配，逗号照吃
            cache.append(';')
            left += 1
            continue

        else:
            raise UnreachableError(
                f"cannot reslove in cache:{left}\n\tcache:\n\t{cache}"
            )

    if bracketlevel != 0:
        print("\n[Warn] Bracket not closed!")
        # 补足右括号
        for i in range(bracketlevel):
            bracketlevel -= 1
            cache.append([')', bracketlevel])
    return cache


def calculate(slice: list) -> float:
    if len(slice) == 1 and isinstance(slice[0], float):
        return slice[0]
    try:
        maxlevel = max(
            [x[1] for x in slice
             if (isinstance(x, list) and x[0] in midclass)]
        )
        i = 0
        while len(slice) != 1:
            try:
                x = slice[i]

                if isinstance(x, list) and x[1] == maxlevel and x[0] in midclass:
                    match x[0]:
                        case '+':
                            slice[i+1] = slice[i-1] + slice[i+1]
                        case '-':
                            slice[i+1] = slice[i-1] - slice[i+1]
                        case '*':
                            slice[i+1] = slice[i-1] * slice[i+1]
                        case '/':
                            try:
                                slice[i+1] = slice[i-1] / slice[i+1]
                            except ZeroDivisionError:
                                raise ExpressionError("Devide by 0")
                        case '%':
                            slice[i+1] = slice[i -
                                               1] % slice[i+1]
                        case '^':
                            slice[i+1] = pow(slice[i-1],
                                             slice[i+1])
                        case 'A', 'P':
                            slice[i+1] = math.perm(int(slice[i-1]),
                                                   int(slice[i+1]))
                        case 'C':
                            slice[i+1] = math.comb(int(slice[i-1]),
                                                   int(slice[i+1]))
                        case _:
                            raise UnreachableError(
                                f"Unknown operator: {x[0]}"
                            )
                    slice.pop(i-1)
                    slice.pop(i-1)
                else:
                    i += 1
            except IndexError:
                # This exception indicates a round have finished
                i = 0
                maxlevel -= 1
                # ShowStep(slice)
    except ValueError:
        if len(slice) == 1 and (isinstance(slice[0], float) or isinstance(slice[0], int)):
            return slice[0]
        else:
            raise UnreachableError(
                f"Unexpected sequence: {slice}"
            )
    if isinstance(slice[0], float):
        return slice[0]
    else:
        raise TypeError


def calculation_breakdown(cache: list[float | str | list]) -> str:
    try:

        maxbracket = max(
            [x[1] for x in cache
             if (isinstance(x, list) and x[0] in Function)]
        )
        left, right, i = [0, 0, 0]
        func = ""
        while maxbracket != -1:
            x = cache[i]
            if isinstance(x, list) and x[1] == maxbracket:
                if len(re.findall('[\\(]', x[0])) != 0:
                    left = i
                    func = x[0]
                elif x[0] == ')':
                    right = i
                    ans = 0
                    match func:
                        case 'log(':
                            # in math module: 真数在前，底数在后
                            # in use: 习惯底数跟在log后
                            match ParameterCounter(cache[left+1:right]):
                                case 1:
                                    print(
                                        "\t[Warn]: Function log() got only one parameter, taking 10 as its base")
                                    log_a = [10]
                                    log_N = cache[left+1:right]
                                case 2:
                                    log_a = cache[left+1:cache.index(';')]
                                    log_N = cache[cache.index(';')+1:right]
                                case _:
                                    raise ExpressionError(
                                        "Too many parameter for log(a,b)")
                            ans = math.log(calculate(log_N), calculate(log_a))
                        case '(':
                            ans = calculate(cache[left+1:right])
                        case _:
                            raise UnreachableError(
                                f"Unknown function: {func}"
                            )
                    for index in range(right - left):
                        cache.pop(left)
                    cache[left] = ans
                    maxbracket = max(
                        [x[1] for x in cache
                         if (isinstance(x, list) and x[0] in Function)]
                    )
                    left, right = [0, 0]
                    i = -1
                    ShowStep(cache)
                else:
                    pass
            else:
                pass
            i += 1
    except ValueError:
        # print_exc()
        # Design for func max() to skip no-bracket sequence
        ShowStep(cache)
        calculate(cache)
        pass
    return str(cache[0])


def solve(cache: list) -> float:
    # schedule
    return 0


def a_mode(expression: str) -> ...:
    l = sys._getframe().f_code.co_name
    print(l)
    input(l+">")
    return


def special_mode(mode: str, expression: str) -> ...:
    # 此处用来放置需要特殊使用的模式
    # 比如无限求和的近似、矩阵高级运算等等
    if mode == "a_mode":
        print("\n\ta_mode activated:")
        a_mode(expression)
        print("\n\ta_mode exiting...:")
    return


midclass = ['+', '-', '*', '/', '%', '^', 'A', 'P', 'C',]
rightclass = ['!']
# changelog: []will no longer be used as general brackets
# changelog: use regex to normalize all bracket
# Lbracket = ['(']
# Rbracket = [')']
Function = [
    'log(', 'ln(',
    'floor(', 'ceil(', 'rand(', 'abs(',
    'sin(', 'cos(', 'tan(', 'arcsin(', 'arccos(', 'arctan(',
    '('
]
# why not consider the right bracket'('as a function
level = [
    ['nothing'],
    ['+', '-'],
    ['*', '/', '%'],
    ['^'],
    ['A', 'P', 'C'],
    ['(', ')']
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
            # 输入，去除空格和前后空白符，替换括号
            expression = input("Basic> ")
            expression = re.sub("[\\s]", '', expression)
            expression = re.sub("[\\[\\{【（]", '(', expression)
            expression = re.sub("[\\]\\}】）]", ')', expression)
            expression = re.sub("[\\,\\;。，；]", ';', expression)
            # Assume that the mode command should act like:
            # MODE:<><mode_name><space|tab><input|none>
            if expression[0: 5].lower() == "mode:":
                i = 0
                for i in range(5, len(expression)):
                    if expression[i] in [' ', '\t']:
                        i -= 1
                        break
                mode = expression[5: i+1]
                if i+1 == len(expression):
                    special_mode(mode, "")
                else:
                    special_mode(mode, expression[i:].lower())
            else:
                # 输入主程序，此步获得输入的完整结构信息
                cache = convert(expression)

                print("\n==> Steps:")
                ShowStep(cache)
                if expression.count("=") == 0:
                    print(f"\nAns={calculation_breakdown(cache)}\n")
                else:
                    solve(cache)

        except EOFError:
            Ans = history.pop()
            print(f"==Undo==> Ans = {Ans}")
        except KeyboardInterrupt:
            exit()
        except ExpressionError as ex:
            print(f"\n[Error][Expression]: {ex.msg} ")
        except UnreachableError as ex:
            print(f"\n[Error][Unreachable]: {ex.msg}")
