import os
import sys
import redis
from board import IBoard
from random import choice
from actionReader import actionReader

redis_info = {
    "host": "127.0.0.1",
    "password": "",
    "port": 6379,
    "db": 0
}
r = redis.Redis(**redis_info, decode_responses=True)


while 1==1:
    myboard = IBoard()
    move_rec = []
    result = None
    while result==None:
        np_board = myboard.getNp()
        np_board = np_board + myboard.player
        move_str = myboard.getNpList()
        if myboard.player == 'r':
            other_side = 'b'
        else:
            other_side = 'r'
        move_arra = move_str.split(',')
        while '' in move_arra:
            move_arra.remove('')
        move_c = move_arra[0]
        search_str_c = r.hget(move_c+other_side, 'search_count')
        value_str_c = r.hget(move_c+other_side,'value')
        if value_str_c != None:
            value_c = int(value_str_c)
        else:
            value_c = 0
        if search_str_c != None:
            search_c = int(search_str_c)
        else:
            search_c = 0
        for move_tmp in move_arra:
            value_str = r.hget(move_tmp+other_side,'value')
            search_str = r.hget(move_tmp + other_side, 'search_count')
            if None == search_str:
                search =0
            else:
                search= int(search_str)
            if None != value_str:
                value = int(value_str)
            else:
                value = 0
            if value-search > value_c-search_c:
                move_c = move_tmp
                value_c = value
            move_rec.append(myboard.getNp()+myboard.player)
            result = myboard.takeActionbyNp(move_c)
    if result == 'r输':
        for arra in move_rec:
            # 检索次数更新
            search_str = r.hget(arra, 'search_count')
            if None != search_str:
                search = int(search_str) + 1
                r.hset(arra, 'search_count', str(search))
            if None == search_str:
                r.hset(arra, 'search_count', '1')
            # 价值更新
            if 'b' in arra:
                value_str = r.hget(arra, 'value')
                if None != value_str:
                    value = int(value_str)-1
                    r.hset(arra, 'value',str(value))
                if None == value_str:
                    r.hset(arra, 'value', '-1')
            if 'r' in arra:
                value_str = r.hget(arra, 'value')
                if None != value_str:
                    value = int(value_str)+1
                    r.hset(arra, 'value',str(value))
                if None == value_str:
                    r.hset(arra, 'value', '1')
    if result == 'b输':
        for arra in move_rec:
            # 检索次数更新
            search_str = r.hget(arra, 'search_count')
            if None != search_str:
                search = int(search_str) + 1
                r.hset(arra, 'search_count', str(search))
            if None == search_str:
                r.hset(arra, 'search_count', '1')
            # 价值更新
            if 'b' in arra:
                value_str = r.hget(arra, 'value')
                if None != value_str:
                    value = int(value_str)+1
                    r.hset(arra, 'value',str(value))
                if None == value_str:
                    r.hset(arra, 'value', '1')
            if 'r' in arra:
                value_str = r.hget(arra, 'value')
                if None != value_str:
                    value = int(value_str)-1
                    r.hset(arra, 'value',str(value))
                if None == value_str:
                    r.hset(arra, 'value', '-1')
    if result == '和':
        for arra in move_rec:
            # 检索次数更新
            search_str = r.hget(arra, 'search_count')
            if None != search_str:
                search = int(search_str) + 1
                r.hset(arra, 'search_count', str(search))
            if None == search_str:
                r.hset(arra, 'search_count', '1')
        value_count = 0
        for cross in myboard.crosses:
            if cross.piece !=None:
                if cross.piece.pieceId == 1 and cross.piece.side =='r':
                    value_count += 9
                if cross.piece.pieceId == 2 and cross.piece.side =='r':
                    value_count += 4
                if cross.piece.pieceId == 3 and cross.piece.side =='r':
                    value_count += 4
                if cross.piece.pieceId == 4 and cross.piece.side =='r':
                    value_count += 2
                if cross.piece.pieceId == 5 and cross.piece.side =='r':
                    value_count += 2
                if cross.piece.pieceId == 6 and cross.piece.side =='r':
                    value_count += 1000
                if cross.piece.pieceId == 7 and cross.piece.side =='r':
                    value_count += 1
                if cross.piece.pieceId == 1 and cross.piece.side =='b':
                    value_count -= 9
                if cross.piece.pieceId == 2 and cross.piece.side =='b':
                    value_count -= 4
                if cross.piece.pieceId == 3 and cross.piece.side =='b':
                    value_count -= 4
                if cross.piece.pieceId == 4 and cross.piece.side =='b':
                    value_count -= 2
                if cross.piece.pieceId == 5 and cross.piece.side =='b':
                    value_count -= 2
                if cross.piece.pieceId == 6 and cross.piece.side =='b':
                    value_count -= 1000
                if cross.piece.pieceId == 7 and cross.piece.side =='b':
                    value_count -= 1
        if value_count>0:
            for arra in move_rec:
                # 价值更新
                if 'b' in arra:
                    value_str = r.hget(arra, 'value')
                    if None != value_str:
                        value = int(value_str) + 1
                        r.hset(arra, 'value', str(value))
                    if None == value_str:
                        r.hset(arra, 'value', '1')
                if 'r' in arra:
                    value_str = r.hget(arra, 'value')
                    if None != value_str:
                        value = int(value_str) - 1
                        r.hset(arra, 'value', str(value))
                    if None == value_str:
                        r.hset(arra, 'value', '-1')
        if value_count<0:
            for arra in move_rec:
                # 价值更新
                if 'b' in arra:
                    value_str = r.hget(arra, 'value')
                    if None != value_str:
                        value = int(value_str) - 1
                        r.hset(arra, 'value', str(value))
                    if None == value_str:
                        r.hset(arra, 'value', '-1')
                if 'r' in arra:
                    value_str = r.hget(arra, 'value')
                    if None != value_str:
                        value = int(value_str) + 1
                        r.hset(arra, 'value', str(value))
                    if None == value_str:
                        r.hset(arra, 'value', '1')