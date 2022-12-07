# encoding=utf-8
'''
Filename : 累加器.py
Datatime : 2022/12/07 
Author :KJH-x
'''


from traceback import print_exc


s = 0
last = 0
while True:
    try:
        i = input().strip()
        if i == "":
            continue
        i = float(i)
        last = s
        s += i
        print(f"==> {s}")
    except TypeError:
        pass
    except EOFError:
        s = last
        print(f"<--Undo-->: {s}")
    except KeyboardInterrupt:
        exit()
    except Exception:
        print_exc()
        input()
