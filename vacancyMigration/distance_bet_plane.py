'''
Descripttion: 
version: 
Author: sch
Date: 2020-10-16 19:22:46
LastEditors: sch
LastEditTime: 2020-10-22 12:25:40
'''
import numpy as np 

# 向量减法
def vector_minus(x, y):
    x = np.array(x)
    y = np.array(y)
    return x - y

# 向量点乘
def inner_product(x, y):
    x = np.array(x)
    y = np.array(y)
    return x[0] * y[0] + x[1] * y[1] + x[2] * y[2]

# 计算两点间的距离
def distance_bet_sites(x, y):
    return np.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2)

# 判断数值是否在合理的误差范围内
def epsilon_criterion(x, standard, epsilon):
    if (standard - epsilon  < x and x < standard + epsilon):
        return True
    else:
        return False


if __name__ == '__main__':
    print(vector_minus([2,2,2], [1,1,1]))
    print(inner_product([1,2,3], [1,2,3]))
    print(distance_bet_sites([1,1,1], [2,2,2]))