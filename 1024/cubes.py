# coding:utf-8

from math import log2, floor
from random import randint
import numpy as np
from pyfiglet import print_figlet
import sys


class CubeMatrix():
    '''
    棋子排布类，核心是实现操作operate'''
    def __init__(self, side_length, test="False"):
        self.__side_length = side_length
        self.__range = np.array([None]*side_length**2).reshape([side_length, side_length])
        for i in range(randint(self.__side_length, floor(self.__side_length**2/2))):
            line = randint(0, self.__side_length-1)
            column = randint(0, self.__side_length-1)
            self.__range[line][column] = Cube()
        if test:
            for i in range(side_length**2):
                line = randint(0, self.__side_length-1)
                column = randint(0, self.__side_length-1)
                self.__range[line][column] = Cube(1)

    def __getitem__(self, index):
        return self.__range[index]

    def operate(self, Super, operation):
        for i in self:
            for j in i:
                if not j is None:
                    j.activate(operation)
        if operation in ["d", "s"]:
            if operation == "d":
                tmp = self.__range
            else:
                tmp = self.__range.T
            for line in range(self.__side_length):
                for column in range(self.__side_length):
                    _line, _column = self.__side_length-line-1, self.__side_length-column-1
                    if not tmp[_line][_column] is None:
                        if not tmp[_line][_column].operation:
                            continue
                        for column2 in range(0, column):
                            _column2 = self.__side_length-column2-1
                            if tmp[_line][_column2] is None:
                                tmp[_line][_column2], tmp[_line][_column] = tmp[_line][_column], None
                                tmp[_line][_column2].operation_done()
                                break
                        else:
                            if column==0:
                                column2 = 0
                                _column2 = self.__side_length-column2-1
                            else:
                                column2 += 1
                                _column2 = self.__side_length-column2-1
                        if column2:
                            if (tmp[_line][_column2] == tmp[_line][_column2+1])&tmp[_line][_column2+1].active:
                                tmp[_line][_column2+1].upgrade()
                                tmp[_line][_column2] = None
        elif operation in ["a", "w"]:
            if operation == "a":
                tmp = self.__range
            else:
                tmp = self.__range.T
            for line in range(self.__side_length):
                for column in range(self.__side_length):
                    if not tmp[line][column] is None:
                        if not tmp[line][column].operation:
                            continue
                        for column2 in range(0, column):

                            if tmp[line][column2] is None:
                                tmp[line][column2], tmp[line][column] = tmp[line][column], None
                                tmp[line][column2].operation_done()
                                break
                        else:
                            if column==0:
                                column2 = 0
                            else:
                                column2 += 1
                        if column2:
                            if (tmp[line][column2] == tmp[line][column2-1])&tmp[line][column2-1].active:
                                tmp[line][column2-1].upgrade()
                                tmp[line][column2] = None

    # def pt(self):
    #     for i in self:
    #         for j in i:
    #             print(j, end="|")
    #         print("\n")
    #     print("+"*20)


class Cube():
    '''
    带数字的方块对象方块'''
    def __init__(self, value=None):
        if value is None:
            import random
            pw = random.randint(0, 3)
            self.value = 2**pw
        else:
            self.value = value
        self.__active = False
        self.__operation = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not isinstance(value, int):
            raise ValueError("value must be int, now {}".format(type(value)))
        if not log2(value).is_integer():
            raise ValueError("value must be powers of 2, now {}".format(value))
        self.__value = value

    @property
    def active(self):
        '''
        acitve属性揭示该方块是否可以接受合并，当operate开始时，所有方块被激活，当某方块和其他方块合并后，该方块激活状态改为False'''
        return self.__active

    @property
    def operation(self):
        '''
        operation属性揭示方块是否移动到位，如方块已经移动到位，operation置为None'''
        return self.__operation

    def operation_done(self):
        '''
        移动操作完成时调用，设置operation为None'''
        self.__operation = None

    def activate(self, op):
        '''
        操作开始时调用'''
        self.__active = True
        self.__operation = op

    def upgrade(self):
        '''
        与其他cube合并，使自身数字翻倍，active置为False，同时判断是否已经完成游戏'''
        self.value = 2*self.value
        self.__active = False
        if self.value > 1023:
            print_figlet("congradulations!")
            sys.exit()

    def __str__(self):
        return " "*(4-len(str(self.value)))+str(self.value)

    def __eq__(self, other):
        if other.__class__ != self.__class__:
            return False
        else:
            if other.value == self.value:
                return True
            else:
                return False


if __name__ == "__main__":
    pass
    