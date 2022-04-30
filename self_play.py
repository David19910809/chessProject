import os
import sys
import redis
from board import IBoard
from actionReader import actionReader

redis_info = {
    "host": "127.0.0.1",
    "password": "",
    "port": 6379,
    "db": 0
}


def pickAction(iboard):
    return None
r = redis.Redis(**redis_info, decode_responses=True)
myboard = IBoard()
while 1==1:
    myboard = IBoard()
        print('电脑预测......')
        np_board = myboard.getNp()
        move_str = r.hget(np_board,'c_node')
        if move_str == None:
            print('电脑认输')
            break
        move_arra = move_str.split(',')
        move_c = move_arra[0]
        value_str_c = r.hget(move_c,'value')
        if value_str_c != None:
            value_c = int(value_str_c)
        else:
            value_c = 0
        for move_tmp in move_arra:
            value_str = r.hget(move_tmp,'value')
            if None != value_str:
                value = int(value_str)
                if value > value_c:
                    move_c = move_tmp
                    value_c = value
        print(move_c)
        myboard.takeActionbyNp(move_c)