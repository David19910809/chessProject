import os
import redis
from board import IBoard
from actionReader import actionReader

redis_info = {
    "host": "127.0.0.1",
    "password": "",
    "port": 6379,
    "db": 0
}
r = redis.Redis(**redis_info, decode_responses=True)
actionReader = actionReader()
flag_board = 1
for filename in os.listdir(r'C://Users//Lucky//Desktop//chess2'):
    file = open('C://Users//Lucky//Desktop//chess2//' + filename)
    actionList = actionReader.getActionList(file)
    iboard = IBoard()
    for action in actionList:
        boardChessActionList = iboard.chessAction()
        flag = 'false'
        for boardAction in boardChessActionList:
            if boardAction.name == action:
                flag = 'true'
        if flag == 'false':
            print('行动非法')
            for action1 in boardChessActionList:
                print(action1.name)
            break
        np = iboard.getNp()
        npList = iboard.getNpList()
        value = r.hget(np,'value')
        if value != None:
            r.hset(np,'value',int(value)+2)
        else:
            r.hset(np, 'value',20)
        r.hset(np,'search_count',0)
        r.hset(np, 'is_expert', 'y')
        r.hset(np, 'c_node', npList)
        iboard.takeAction(action)
    flag_board+=1
    print('完成训练第'+str(flag_board)+'盘')
# r.hset(np_info,'value',20)
# r.hset(np_info,'searchCount',20)

# board = IBoard()
# print(board.getNp())
# tmp = board.getNpList()
# print(tmp)
# for arra in tmp:
    # print(''.join(str(i) for i in arra))

