import numpy as np

#1.将棋盘视为一个封闭的环境
#2.红方的分值为：子力价值+占位价值+控制点位价值+先手价值
#3.以人类专家动作作为最佳实践训练模型。

#棋盘子力价值
#9,4,2,2,1000,2,2,4,9
#0,0,0,0,0,0,0,0,0
#0,4,0,0,0,0,0,4,0
#1,0,1,0,1,0,1,0,1
#0,0,0,0,0,0,0,0,0
#0,0,0,0,0,0,0,0,0
#1,0,1,0,1,0,1,0,1
#0,4,0,0,0,0,0,4,0
#0,0,0,0,0,0,0,0,0
#9,4,2,2,1000,2,2,4,9

#棋盘位置价值
#1,1,1,1,1,1,1,1,1
#1,1,1,1,1,1,1,1,1
#1,1,1,1,1,1,1,1,1
#1,1,1,1,1,1,1,1,1
#1,1,1,1,1,1,1,1,1
#1,1,1,1,1,1,1,1,1
#1,1,1,1,1,1,1,1,1
#1,1,1,1,1,1,1,1,1
#1,1,1,1,1,1,1,1,1
#1,1,1,1,1,1,1,1,1

#棋盘位置信息,对称性
#[(x,y),(x1,y1),,,,]
class IPiece:
    def __init__(self,side,pieceId,isDead,value,name):
        self.side = side
        self.pieceId = pieceId
        self.isDead = isDead
        self.value = value
        self.name = name

class ICross:
    def __init__(self,rx,ry,bx,by,piece,value):
        self.rx = rx
        self.ry = ry
        self.bx = bx
        self.by = by
        self.piece = piece
        self.value = value


class IBoard:
    def __init__(self):
        self.player = 'r'
        self.cross1 = ICross(1, 0, 9, 9, IPiece('r', 1, 'n', 9, '车'),1)
        self.cross2 = ICross(2, 0, 8, 9, IPiece('r', 3, 'n', 4, '马'),1)
        self.cross3 = ICross(3, 0, 7, 9, IPiece('r', 4, 'n', 2, '相'),1)
        self.cross4 = ICross(4, 0, 6, 9, IPiece('r', 5, 'n', 2, '士'),1)
        self.cross5 = ICross(5, 0, 5, 9, IPiece('r', 6, 'n', 1000, '将'),1)
        self.cross6 = ICross(6, 0, 4, 9, IPiece('r', 5, 'n', 2, '士'),1)
        self.cross7 = ICross(7, 0, 3, 9, IPiece('r', 4, 'n', 2, '相'),1)
        self.cross8 = ICross(8, 0, 2, 9, IPiece('r', 3, 'n', 4, '马'),1)
        self.cross9 = ICross(9, 0, 1, 9, IPiece('r', 1, 'n', 9, '车'),1)
        self.cross10 = ICross(1, 1, 9, 8, None,1)
        self.cross11 = ICross(2, 1, 8, 8, None,1)
        self.cross12 = ICross(3, 1, 7, 8, None,1)
        self.cross13 = ICross(4, 1, 6, 8, None,1)
        self.cross14 = ICross(5, 1, 5, 8, None,1)
        self.cross15 = ICross(6, 1, 4, 8, None,1)
        self.cross16 = ICross(7, 1, 3, 8, None,1)
        self.cross17 = ICross(8, 1, 2, 8, None,1)
        self.cross18 = ICross(9, 1, 1, 8, None,1)
        self.cross19 = ICross(1, 2, 9, 7, None,1)
        self.cross20 = ICross(2, 2, 8, 7, IPiece('r', 2, 'n', 4, '炮'),1)
        self.cross21 = ICross(3, 2, 7, 7, None,1)
        self.cross22 = ICross(4, 2, 6, 7, None,1)
        self.cross23 = ICross(5, 2, 5, 7, None,1)
        self.cross24 = ICross(6, 2, 4, 7, None,1)
        self.cross25 = ICross(7, 2, 3, 7, None,1)
        self.cross26 = ICross(8, 2, 2, 7, IPiece('r', 2, 'n', 4, '炮'),1)
        self.cross27 = ICross(9, 2, 1, 7, None,1)
        self.cross28 = ICross(1, 3, 9, 6, IPiece('r', 1, 'n', 9, '兵'),1)
        self.cross29 = ICross(2, 3, 8, 6, None,1)
        self.cross30 = ICross(3, 3, 7, 6, IPiece('r', 1, 'n', 9, '兵'),1)
        self.cross31 = ICross(4, 3, 6, 6, None,1)
        self.cross32 = ICross(5, 3, 5, 6, IPiece('r', 1, 'n', 9, '兵'),1)
        self.cross33 = ICross(6, 3, 4, 6, None,1)
        self.cross34 = ICross(7, 3, 3, 6, IPiece('r', 1, 'n', 9, '兵'),1)
        self.cross35 = ICross(8, 3, 2, 6, None,1)
        self.cross36 = ICross(9, 3, 1, 6, IPiece('r', 1, 'n', 9, '兵'),1)
        self.cross37 = ICross(1, 4, 9, 5, None,1)
        self.cross38 = ICross(2, 4, 8, 5, None,1)
        self.cross39 = ICross(3, 4, 7, 5, None,1)
        self.cross40 = ICross(4, 4, 6, 5, None,1)
        self.cross41 = ICross(5, 4, 5, 5, None,1)
        self.cross42 = ICross(6, 4, 4, 5, None,1)
        self.cross43 = ICross(7, 4, 3, 5, None,1)
        self.cross44 = ICross(8, 4, 2, 5, None,1)
        self.cross45 = ICross(9, 4, 1, 5, None,1)
        self.cross46 = ICross(1, 5, 9, 4, None,1)
        self.cross47 = ICross(2, 5, 8, 4, None,1)
        self.cross48 = ICross(3, 5, 7, 4, None,1)
        self.cross49 = ICross(4, 5, 6, 4, None,1)
        self.cross50 = ICross(5, 5, 5, 4, None,1)
        self.cross51 = ICross(6, 5, 4, 4, None,1)
        self.cross52 = ICross(7, 5, 3, 4, None,1)
        self.cross53 = ICross(8, 5, 2, 4, None,1)
        self.cross54 = ICross(9, 5, 1, 4, None,1)
        self.cross55 = ICross(1, 6, 9, 3, IPiece('b', 1, 'n', 9, '兵'),1)
        self.cross56 = ICross(2, 6, 8, 3, None,1)
        self.cross57 = ICross(3, 6, 7, 3, IPiece('b', 1, 'n', 9, '兵'),1)
        self.cross58 = ICross(4, 6, 6, 3, None,1)
        self.cross59 = ICross(5, 6, 5, 3, IPiece('b', 1, 'n', 9, '兵'),1)
        self.cross60 = ICross(6, 6, 4, 3, None,1)
        self.cross61 = ICross(7, 6, 3, 3, IPiece('b', 1, 'n', 9, '兵'),1)
        self.cross62 = ICross(8, 6, 2, 3, None,1)
        self.cross63 = ICross(9, 6, 1, 3, IPiece('b', 1, 'n', 9, '兵'),1)
        self.cross64 = ICross(1, 7, 9, 2, None,1)
        self.cross65 = ICross(2, 7, 8, 2, IPiece('b', 2, 'n', 4, '炮'),1)
        self.cross66 = ICross(3, 7, 7, 2, None,1)
        self.cross67 = ICross(4, 7, 6, 2, None,1)
        self.cross68 = ICross(5, 7, 5, 2, None,1)
        self.cross69 = ICross(6, 7, 4, 2, None,1)
        self.cross70 = ICross(7, 7, 3, 2, None,1)
        self.cross71 = ICross(8, 7, 2, 2, IPiece('b', 2, 'n', 4, '炮'),1)
        self.cross72 = ICross(9, 7, 1, 2, None,1)
        self.cross73 = ICross(1, 8, 9, 1, None,1)
        self.cross74 = ICross(2, 8, 8, 1, None,1)
        self.cross75 = ICross(3, 8, 7, 1, None,1)
        self.cross76 = ICross(4, 8, 6, 1, None,1)
        self.cross77 = ICross(5, 8, 5, 1, None,1)
        self.cross78 = ICross(6, 8, 4, 1, None,1)
        self.cross79 = ICross(7, 8, 3, 1, None,1)
        self.cross80 = ICross(8, 8, 2, 1, None,1)
        self.cross81 = ICross(9, 8, 1, 1, None,1)
        self.cross82 = ICross(1, 9, 9, 0, IPiece('b', 1, 'n', 9, '车'),1)
        self.cross83 = ICross(2, 9, 8, 0, IPiece('b', 3, 'n', 4, '马'),1)
        self.cross84 = ICross(3, 9, 7, 0, IPiece('b', 4, 'n', 2, '相'),1)
        self.cross85 = ICross(4, 9, 6, 0, IPiece('b', 5, 'n', 2, '士'),1)
        self.cross86 = ICross(5, 9, 5, 0, IPiece('b', 6, 'n', 1000, '将'),1)
        self.cross87 = ICross(6, 9, 4, 0, IPiece('b', 5, 'n', 2, '士'),1)
        self.cross88 = ICross(7, 9, 3, 0, IPiece('b', 4, 'n', 2, '相'),1)
        self.cross89 = ICross(8, 9, 2, 0, IPiece('b', 3, 'n', 4, '马'),1)
        self.cross90 = ICross(9, 9, 1, 0, IPiece('b', 1, 'n', 9, '车'),1)
        self.crosses = [self.cross1,self.cross2,self.cross3,self.cross4,self.cross5,self.cross6,self.cross7,self.cross8,self.cross9,
                        self.cross10, self.cross11, self.cross12, self.cross13, self.cross14, self.cross15, self.cross16,
                        self.cross17, self.cross18,
                        self.cross19, self.cross20, self.cross21, self.cross22, self.cross23, self.cross24, self.cross25,
                        self.cross26, self.cross27,
                        self.cross28, self.cross29, self.cross30, self.cross31, self.cross32, self.cross33, self.cross34,
                        self.cross35, self.cross36,
                        self.cross37, self.cross38, self.cross39, self.cross40, self.cross41, self.cross42, self.cross43,
                        self.cross44, self.cross45,
                        self.cross46, self.cross47, self.cross48, self.cross49, self.cross50, self.cross51, self.cross52,
                        self.cross53, self.cross54,
                        self.cross55, self.cross56, self.cross57, self.cross58, self.cross59, self.cross60, self.cross61,
                        self.cross62, self.cross63,
                        self.cross64, self.cross65, self.cross66, self.cross67, self.cross68, self.cross69, self.cross70,
                        self.cross71, self.cross72,
                        self.cross73, self.cross74, self.cross75, self.cross76, self.cross77, self.cross78, self.cross79,
                        self.cross80, self.cross81,
                        self.cross82, self.cross83, self.cross84, self.cross85, self.cross86, self.cross87, self.cross88,
                        self.cross89, self.cross90
                        ]

    def getAllAction(self):
        #遍历所有子力位置的交叉点，得到所有的行动子集。
        #print('nihao')
        for cross in self.crosses:
        # for cross in self.crosses:
        #     if(cross.rx%9 ==0):
        #         if (cross.piece != None):
        #             print(cross.piece.name)
        #         else:
        #             print("——")
        #     else:
        #         if (cross.piece != None):
        #             print(cross.piece.name,end="")
        #         else:
        #             print("——",end="")
    # 工具方法，根据坐标返回相应的交叉点
    def getCrossByCoordinate(self,x,y,side):
        if side == 'b':
            for cross in self.crosses:
                if x == cross.bx and y == cross.by:
                    return cross
        if side == 'r':
            for cross in self.crosses:
                if x == cross.rx and y == cross.ry:
                    return cross
    #返回每个棋子的可达交叉点，即控制交叉点
    def getPieceControl(self,cross):
        # 车的走法
        controlList = []
        if cross.piece.pieceId == 1:
            rx = cross.piece.rx
            ry = cross.piece.ry

            else:



if __name__ == '__main__':
    myboard = IBoard()
    myboard.getAllAction()

