# coding:utf-8

from math import log2, floor
from random import randint
from cubes import Cube, CubeMatrix
import re
from pyfiglet import print_figlet


class Board():
    '''
    游戏棋盘，初始化参数传入棋盘边长'''
    def __init__(self, side_length):
        if not isinstance(side_length, int):
            raise TypeError("digit needed, {} {} given".format(type(side_length), side_length))
        self.__side_length = side_length
        self.__range = CubeMatrix(side_length)

    @property
    def side_length(self):
        '''
        只读属性，棋盘边长'''
        return self.__side_length

    # @side_length.setter
    # def side_length(self, value):
    #     if value<4:
    #         raise ValueError("Board.side_length should gt 4, now {}".format(value))
    #     self.__side_length = value

    def __str__(self):
        '''
        定义格式化输出方式（命令行）'''
        batch = ""
        for i in self.__range:
            batch += "-"*5*self.__side_length+"-\n|"
            for j in i:
                if j is None:
                    batch += " "*4+"|"
                else:
                    batch += str(j)+"|"
            batch += "\n"
        batch += "-"*5*self.__side_length+"\n"
        print(self.cube_count)
        return batch

    def get_cube_min(self):
        '''
        获取当前最小的cube（数字方块）'''
        value = 2048
        for i in self.__range:
            for j in i:
                if j is None:
                    continue
                if j.value < value:
                    value = j.value
        return value

    def get_cube_max(self):
        '''
        获取当前最大的cube（数字方块）'''
        value = 0
        for i in self.__range:
            for j in i:
                if j is None:
                    continue
                if j.value > value:
                    value = j.value
        return value

    def count_cube(self, value):
        '''
        数出当前棋盘的某个数字值的cube数'''
        if not isinstance(value, int):
            raise ValueError("value must be int, now {}".format(type(value)))
        if not log2(value).is_integer():
            raise ValueError("value must be powers of 2, now {}".format(value))
        count = 0
        for i in self.__range:
            for j in i:
                if j is None:
                    continue
                if j.value == value:
                    count += 1
        return count

    @property
    def cube_count(self):
        '''
        只读属性，棋盘上的cube数'''
        count = 0
        for i in self.__range:
            for j in i:
                if not j is None:
                    count += 1
        return count

    # def init_board(self):
    #     self.__range = [[None for _ in range(self.__side_length)] for _i in range(self.__side_length)]
    #     for i in range(randint(self.__side_length, floor(self.__side_length**2/2))):
    #         line = randint(0, self.__side_length-1)
    #         column = randint(0, self.__side_length-1)
    #         self.__range[line][column] = Cube()
    #     print(self)

    def appear_random(self):
        '''
        在随机位置出现一些新cube'''
        def appear(value):
            while True:
                line = randint(0, self.__side_length-1)
                column = randint(0, self.__side_length-1)
                if self.__range[line][column] is None:
                    self.__range[line][column] = Cube(value)
                    break
        min_cube = self.get_cube_min()
        max_cube = self.get_cube_max()
        for i in range(4): # 一次添加最多四个方块
            if max_cube==min_cube:
                pass
            else:
                max_cube = max_cube/2
            pw = randint(int(log2(min_cube)), int(log2(max_cube)))
            if randint(0, 1):
                appear(2**pw)
        if self.count_cube(min_cube)%2: # 如果最小方块个数为奇数的话，添加一个最小方块
            appear(min_cube)

    def shuffle(self, force=False):
        '''
        当方块数量少于棋盘面积的1/3时，为棋盘随机添加0-5个方块。
        如果指定force为True，则强制添加1或2个方块'''
        while True:
            if force:
                self.appear_random()
                break
            if self.cube_count < 1/3*self.__side_length**2:
                self.appear_random()
            else:
                break

    def operate(self, operation):
        '''
        用户操作，接受操作(wasd)s'''
        self.__range.operate(self, operation)
        self.shuffle()


if __name__ == "__main__":
    pass


