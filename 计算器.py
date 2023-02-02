# encoding=utf-8
# python_version>=3.10
'''
Filename : 累加器.py
Datatime : 2022/12/07
Author :KJH-x
'''

from traceback import print_exc
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


class NohistoryError(IndexError):
    """Pop expression from empty history list

    Args:
        IndexError (_type_): _description_
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
    isolateContent = re.sub("(\\.0[\\,\\]]{1})", '', f"{isolateContent}")
    isolateContent = re.sub("[\\[\\]\\,\\'\\s]", '', isolateContent)
    isolateContent = re.sub("\\;", ',', isolateContent)

    print(f'\t{isolateContent}')
    return


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


def iscomplex(expression: str) -> bool:
    """Judge if the expression is an acceptble complex number
    """
    # new
    return False


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
    global ans, last, history
    if command in ['part', 'full']:
        ans = 0
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
    mode = ''
    left, right = [0, 0]
    # 括号优先级计算，左括号加一级，右括号减一级
    # 输入的括号可不在形式上成对，只要左右个数一致即可
    bracketlevel = 0
    # 输入分析：
    while left < len(expression):
        number = 0
        if re.match("[0-9\\.]", expression[left]):
            # 过程量记录
            for right in range(left+1, len(expression)+1):
                test = expression[left:right]
                if re.match(pattern[0][0], test) \
                        or re.match(pattern[0][1], test)\
                        or re.match(pattern[1][0], test)\
                        or re.match(pattern[1][1], test):
                    number = float(test)
                elif test == '.':
                    pass
                elif re.match(pattern[2][0], test)\
                        or re.match(pattern[2][1], test):
                    if re.match(pattern[3][0], test)\
                            or re.match(pattern[3][1], test):
                        right -= 1
                        break
                    else:
                        pass
                else:
                    right -= 1
                    break

            cache.append(float(number))
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

        elif re.match(f"[^0-9{keyword}]", expression[left]):
            # 记录函数、变量、左括号
            # 同时还要处理变量
            test = ''
            function = ''
            variable = ''
            for right in range(left+1, len(expression)+1):
                test = str(expression[left:right])
                if re.match(pat_func, test):
                    function = test
                    break
                elif re.match(pat_var, test):
                    variable = test
                else:
                    right -= 1
                    break

            # 如果前面一个是数字，那么是缩写，把没有的乘号补上
            if len(cache) > 0 and isinstance(cache[-1], float):
                cache.append(assign_class('*'))

            if function == '':
                if variable != 'set':
                    if mode != 'set_var':
                        try:
                            cache.append(var_dict[variable])
                            right if right else right
                        except KeyError:
                            var_dict[variable] = 0.0
                            raise ExpressionError(
                                f"Unknown varibale {variable}, created"
                            )
                    else:
                        cache.append(variable)
                        mode = ''
                else:
                    mode = 'set_var'
                    right += 1

            else:
                # 记录的时候记录函数名称
                cache.append([function, bracketlevel])
                # last_type = function
                bracketlevel += 1
            left = right
            continue

        elif expression[left] == ')':
            # 遇到右侧等号，处理前减一级
            bracketlevel -= 1
            cache.append([str(expression)[left], bracketlevel])
            left += 1
            continue

        elif expression[left] in [';', '=']:
            # 多个参数不好处理，由拆分函数执行任务分配，逗号照吃
            # 等号作判断用，照吃
            cache.append(expression[left])
            left += 1
            continue

        else:
            raise UnreachableError(
                f"cannot reslove in expression:{left}\n\texpression:\n\t{expression}"
            )

    if bracketlevel != 0:
        print("\n[Warn] Bracket not closed!")
        # 补足右括号
        for i in range(bracketlevel):
            bracketlevel -= 1
            cache.append([')', bracketlevel])
    return cache


def calculate(slice: list) -> float:
    for index in range(len(slice)):
        if isinstance(slice[index], list) and slice[index][0] in ['(', ')']:
            slice.pop(index)
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
                    try:
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
                    except TypeError:
                        raise ExpressionError(
                            f"Adjacent operator, check expression"
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


def calculation_breakdown(cache: list) -> float:
    try:
        if len(cache) == 1:
            return float(cache[0])
        maxbracket = max(
            [x[1] for x in cache
             if (isinstance(x, list) and x[0] in functions)]
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
                                    log_a = [10.0]
                                    log_N = cache[left+1:right]
                                case 2:
                                    log_a = cache[left + 1:
                                                  cache[left+1:right].index(';')+left+1]
                                    log_N = cache[cache[left+1:right].index(';')+left+2:
                                                  right+1]
                                case _:
                                    raise ExpressionError(
                                        "Too many parameter for log(a,b)"
                                    )
                            try:
                                ans = math.log(
                                    calculate(log_N), calculate(log_a)
                                )
                            except ZeroDivisionError:
                                raise ExpressionError(
                                    f"log(1,x)"
                                )
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
                         if (isinstance(x, list) and x[0] in functions)]
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
        ShowStep(cache) if len(cache) > 2 else 1
        calculate(cache)
        pass
    return float(cache[0])


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
functions = [
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


var_dict = dict()
var_dict['ans'] = 0
last = 0
history = []

keyword = "\\+\\-\\*\\/\\%\\= \\;\\) \\."
gt0 = "{0,}"
gt1 = "{1,}"
eq1 = "{1}"

# pat_func = f"^[^0-9 \\+\\-\\*\\/\\%\\= ;\\)]{0,}[^\\+\\-\\*\\/\\%\\= ;\\)\\(]{0,}[\\()]$"
pat_func = f"^[^0-9{keyword}]{gt0}[^{keyword}\\(]{gt0}[\\()]$"
# 函数的正则模式：
#    开头： 非（数字，算符，分隔符，右括号）
#    中间：任意长度（大于等于0）的 非（算符，分隔符，右括号）
#    结尾：右括号
pat_var = f"^[^0-9{keyword}]{eq1}[^{keyword}\\(]{gt0}$"
# 变量的正则模式：
#    开头： 非（数字，算符，分隔符，右括号）
#    中间：任意长度（大于等于0）的 非（算符，分隔符，右括号）
#    结尾：非右括号，通过先判断是否为函数
pattern = [
    [
        "(^[0-9]{1,}([\\.][0-9]{0,}){0,1}$)",
        # 'xx' 'xx.xx' 'xx.'
        "^[\\.][0-9]{1,}$",
        # '.xx'
    ],
    [
        "^[0-9]{1,}([.\\][0-9]{0,}){0,}e(\\+|\\-){0,1}[0-9]{1,}$",
        # 'xxe+-xx', 'xx.e+-xx', 'xx.xxe+-xx ...etc'
        "^[\\.][0-9]{1,}e(\\+|\\-){0,1}[0-9]{1,}$",
        # '.xxe+-xx ...etc'
    ],
    [
        "^[0-9]{1,}([.\\][0-9]{0,}){0,}e",
        # 'xx.xxe... insufficient'
        "^[\\.][0-9]{1,}e",
        # '.xxe... insufficient'
    ],
    [
        "^[0-9]{1,}([.\\][0-9]{0,}){0,}e(\\+|\\-){0,1}[0-9]{1,}.{1,}",
        # 'xx.xxe+-xx?... overflow'
        "^[\\.][0-9]{1,}e(\\+|\\-){0,1}[0-9]{1,}.{1,}",
        # '.xxe+-xx?... overflow'
    ]
]

if __name__ == '__main__':

    memory = []
    last_type = ""
    flash()
    while True:
        try:
            # 输入，去除空格和前后空白符，替换括号
            expression = input("Basic> ").lower().strip()
            # expression = re.sub("[\\s]", '', expression)
            expression = re.sub("[\\[\\{【（]", '(', expression)
            expression = re.sub("[\\]\\}】）]", ')', expression)
            expression = re.sub("[\\,\\;。，；]", ';', expression)
            # Assume that the mode command should act like:
            # MODE:<><mode_name><space|tab><input|none>
            if expression[0] == '+':
                expression = 'ans'+expression

            if expression[0:5].lower() == "mode:":
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
            elif expression[0:3] == 'set':
                expression = 'set '+re.sub("[\\s]", '', expression[3:])
                cache = convert(expression)
                try:
                    if len(cache[cache.index('=')+1:]) > 1:
                        print("\n==> Steps:")
                        ShowStep(cache)
                    var_value = calculation_breakdown(
                        cache[cache.index('=')+1:])
                    var_dict[cache[0]] = var_value
                    print(f"\n[Info] Variable {cache[0]} set to {var_value}\n")
                except ValueError:
                    raise ExpressionError(
                        f"No '=' in assignment syntax"
                    )
                history.append(cache)
            else:
                expression = re.sub("[\\s]", '', expression)
                # 输入主程序，此步获得输入的完整结构信息
                cache = convert(expression)
                if [x for x in cache if isinstance(x, float)] == []:
                    pass
                else:
                    if len(cache) > 1:
                        print("\n==> Steps:")
                        ShowStep(cache)
                    history_cache = copy.deepcopy(cache)
                    history.append(history_cache)
                    del history_cache
                    if expression.count("=") == 0:
                        var_dict['ans'] = calculation_breakdown(cache)
                        print(f"\nAns={var_dict['ans']}\n")
                    else:
                        solve(cache)

        except EOFError:
            try:
                var_dict['ans'] = history.pop()
                print(f"==Undo==> Ans = {var_dict['ans']}")
            except IndexError:
                try:
                    raise NohistoryError("Empty History")
                except NohistoryError as ex:
                    print(f"\n[Warn][History]: {ex.msg}")
        except KeyboardInterrupt:
            exit()
        except ExpressionError as ex:
            print(f"\n[Error][Expression]: {ex.msg} ")
        except UnreachableError as ex:
            print(f"\n[Error][Unreachable]: {ex.msg}")

        except Exception:
            if input("[Exception] type 1 to see detail") == '1':
                print_exc()
