from math import *
import numpy as np
import utils

GRID_WIDTH = 40

COLUMN = 15
ROW = 15

DEPTH = 3  # 搜索深度

list1 = []  # AI
list2 = []  # 人
list3 = []  # 全部棋子

list_all = []  # 整个棋盘的点
next_point = (0, 0)  # AI下一步最应该下的位置

shape_score = [(50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),
               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),
               (5000, (1, 1, 1, 0, 1)),
               (5000, (1, 1, 0, 1, 1)),
               (5000, (1, 0, 1, 1, 1)),
               (5000, (1, 1, 1, 1, 0)),
               (5000, (0, 1, 1, 1, 1)),
               (50000, (0, 1, 1, 1, 1, 0)),
               (99999999, (1, 1, 1, 1, 1))] #一些简单的棋形 还需要考虑禁手

def agent():
    minimax(0, DEPTH, -99999999, 99999999)
    return next_point

#agentIndex就是判断AI执黑还是执白取0 1
def minimax(agentIndex, depth, alpha, beta):
    if isWin(list1) or isWin(list2) or depth == 0:
        return evaluation(agentIndex)
    
    blank_list = list(set(list_all).difference(set(list3)))
    order(blank_list)

    for next_step in blank_list:
        # 如果要评估的位置没有相邻的棋子,则不去评估
        if not has_neightnor(next_step):
            continue
        if agentIndex:
            list1.append(next_step)
        else:
            list2.append(next_step)
        list3.append(next_step)

        value = -minimax((-agentIndex)+1, depth - 1, -beta, -alpha)

        if agentIndex:
            list1.remove(next_step)
        else:
            list2.remove(next_step)
        list3.remove(next_step)

        if value > alpha:
            if depth == DEPTH:
                next_point[0] = next_step[0]
                next_point[1] = next_step[1]
            #剪枝
            if value >= beta:
                global cut_count
                cut_count += 1
                return beta
            alpha = value
    return alpha

#判断是不是已经有人胜利了
def isWin(list):
    for m in range(COLUMN):
        for n in range(ROW):
            if n < ROW - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (m, n + 3) in list and (m, n + 4) in list:
                return True
            elif m < ROW - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (m + 3, n) in list and (m + 4, n) in list:
                return True
            elif m < ROW - 4 and n < ROW - 4 and (m, n) in list and (m + 1, n + 1) in list and (m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
                return True
            elif m < ROW - 4 and n > 3 and (m, n) in list and (m - 1, n + 1) in list and (m - 2, n + 2) in list and (m - 3, n + 3) in list and (m - 4, n + 4) in list:
                return True
    return False

#判断评估位置周围有没有棋子
def has_neightnor(pt):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1] + j) in list3:
                return True
    return False

#评价函数，算AI的分
def evaluation(agentIndex):
    score = 0
    #AI执黑白由agentIndex, 初始化list
    if agentIndex:
        my_list = list1
        enemy_list = list2
    else:
        my_list = list2
        enemy_list = list1
    #记录该方向分数最高的形状
    score_arr = []
    #分数
    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        #四个方向，横竖对角
        my_score += cal_score(m, n, 0, 1, enemy_list, my_list, score_arr)
        my_score += cal_score(m, n, 1, 0, enemy_list, my_list, score_arr)
        my_score += cal_score(m, n, 1, 1, enemy_list, my_list, score_arr)
        my_score += cal_score(m, n, -1, 1, enemy_list, my_list, score_arr)

    #对手
    score_arr_enemy = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score(m, n, 0, 1, enemy_list, my_list, score_arr_enemy)
        enemy_score += cal_score(m, n, 1, 0, enemy_list, my_list, score_arr_enemy)
        enemy_score += cal_score(m, n, 1, 1, enemy_list, my_list, score_arr_enemy)
        enemy_score += cal_score(m, n, -1, 1, enemy_list, my_list, score_arr_enemy)

    score = my_score - enemy_score
    return score

#计算该点位得分
def cal_score(m, n, x_direct, y_direct, enemy_list, my_list, score_arr):
    add_score = 0
    max_score_shape = (0, None)

    for item in score_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_direct == item[2][0] and y_direct == item[2][1]:
                return 0
    
    for offset in range(-5, 1):
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_direct, n + (i + offset) * y_direct) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_direct, n + (i + offset) * y_direct) in my_list:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                if tmp_shap5 == (1,1,1,1,1):
                    #晚点处理
                    continue
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+offset) * x_direct, n + (0+offset) * y_direct),
                                               (m + (1+offset) * x_direct, n + (1+offset) * y_direct),
                                               (m + (2+offset) * x_direct, n + (2+offset) * y_direct),
                                               (m + (3+offset) * x_direct, n + (3+offset) * y_direct),
                                               (m + (4+offset) * x_direct, n + (4+offset) * y_direct)), (x_direct, y_direct))
    #对比棋形，有俩不一样的形状，分更高
    if max_score_shape[1] is not None:
        for item in score_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]
        score_arr.append(max_score_shape)
    
    return add_score+max_score_shape[0]
        
def order(blank_list):
    last_pt = list3[-1]
    for _ in blank_list:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                    blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                    blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))
