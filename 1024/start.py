# coding:utf-8

import re
from board import Board


if __name__ == "__main__":
    side = input("input board width(4-9): ")
    match = re.match("[456789]{1}", side)
    while match is None:
        side = input("input board width(4-9): ")
        match = re.match("[456789]{1}", side)
    side = match.group(0)
    b = Board(int(side))
    pat = re.compile("[wsad]{1}")
    while True:
        print(b)
        o = input("input operation(wasd): ")
        if o == "e":
            b.shuffle(True)
        if o == "q":
            print_figlet("see you!")
            break
        else:
            ops = pat.findall(o)
            if o == []:
                print("input valid operation(wasd)")
            for i in o:
                b.operate(i)


