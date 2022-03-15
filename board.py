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

#棋盘位置信息
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
        self.cross1 = ICross(1, 0, 9, 9, IPiece('r', 1, 'n', 9, '车'))
        self.cross2 = ICross(2, 0, 8, 9, IPiece('r', 3, 'n', 4, '马'))
        self.cross3 = ICross(3, 0, 7, 9, IPiece('r', 4, 'n', 2, '相'))
        self.cross4 = ICross(4, 0, 6, 9, IPiece('r', 5, 'n', 2, '士'))
        self.cross5 = ICross(5, 0, 5, 9, IPiece('r', 6, 'n', 1000, '将'))
        self.cross6 = ICross(6, 0, 4, 9, IPiece('r', 5, 'n', 2, '士'))
        self.cross7 = ICross(7, 0, 3, 9, IPiece('r', 4, 'n', 2, '相'))
        self.cross8 = ICross(8, 0, 2, 9, IPiece('r', 3, 'n', 4, '马'))
        self.cross9 = ICross(9, 0, 1, 9, IPiece('r', 1, 'n', 9, '车'))

        self.cross10 = ICross(1, 1, 9, 8, None)
        self.cross11 = ICross(2, 1, 8, 8, None)
        self.cross12 = ICross(3, 1, 7, 8, None)
        self.cross13 = ICross(4, 1, 6, 8, None)
        self.cross14 = ICross(5, 1, 5, 8, None)
        self.cross15 = ICross(6, 1, 4, 8, None)
        self.cross16 = ICross(7, 1, 3, 8, None)
        self.cross17 = ICross(8, 1, 2, 8, None)
        self.cross18 = ICross(9, 1, 1, 8, None)


        self.cross19 = ICross(1, 2, 9, 7, None)
        self.cross20 = ICross(2, 2, 8, 7, IPiece('r', 2, 'n', 4, '炮'))
        self.cross21 = ICross(3, 2, 7, 7, None)
        self.cross22 = ICross(4, 2, 6, 7, None)
        self.cross23 = ICross(5, 2, 5, 7, None)
        self.cross24 = ICross(6, 2, 4, 7, None)
        self.cross25 = ICross(7, 2, 3, 7, None)
        self.cross26 = ICross(8, 2, 2, 7, IPiece('r', 2, 'n', 4, '炮'))
        self.cross27 = ICross(9, 2, 1, 7, None)


        self.cross28 = ICross(1, 3, 9, 6, IPiece('r', 1, 'n', 9, '兵'))
        self.cross29 = ICross(2, 3, 8, 6, None)
        self.cross30 = ICross(3, 3, 7, 6, IPiece('r', 1, 'n', 9, '兵'))
        self.cross31 = ICross(4, 3, 6, 6, None)
        self.cross32 = ICross(5, 3, 5, 6, IPiece('r', 1, 'n', 9, '兵'))
        self.cross33 = ICross(6, 3, 4, 6, None)
        self.cross34 = ICross(7, 3, 3, 6, IPiece('r', 1, 'n', 9, '兵'))
        self.cross35 = ICross(8, 3, 2, 6, None)
        self.cross36 = ICross(9, 3, 1, 6, IPiece('r', 1, 'n', 9, '兵'))


        self.cross37 = ICross(1, 4, 9, 5, None)
        self.cross38 = ICross(2, 4, 8, 5, None)
        self.cross39 = ICross(3, 4, 7, 5, None)
        self.cross40 = ICross(4, 4, 6, 5, None)
        self.cross41 = ICross(5, 4, 5, 5, None)
        self.cross42 = ICross(6, 4, 4, 5, None)
        self.cross43 = ICross(7, 4, 3, 5, None)
        self.cross44 = ICross(8, 4, 2, 5, None)
        self.cross45 = ICross(9, 4, 1, 5, None)


        self.cross46 = ICross(1, 5, 9, 4, None)
        self.cross47 = ICross(2, 5, 8, 4, None)
        self.cross48 = ICross(3, 5, 7, 4, None)
        self.cross49 = ICross(4, 5, 6, 4, None)
        self.cross50 = ICross(5, 5, 5, 4, None)
        self.cross51 = ICross(6, 5, 4, 4, None)
        self.cross52 = ICross(7, 5, 3, 4, None)
        self.cross53 = ICross(8, 5, 2, 4, None)
        self.cross54 = ICross(9, 5, 1, 4, None)


        self.cross55 = ICross(1, 6, 9, 3, IPiece('b', 1, 'n', 9, '兵'))
        self.cross56 = ICross(2, 6, 8, 3, None)
        self.cross57 = ICross(3, 6, 7, 3, IPiece('b', 1, 'n', 9, '兵'))
        self.cross58 = ICross(4, 6, 6, 3, None)
        self.cross59 = ICross(5, 6, 5, 3, IPiece('b', 1, 'n', 9, '兵'))
        self.cross60 = ICross(6, 6, 4, 3, None)
        self.cross61 = ICross(7, 6, 3, 3, IPiece('b', 1, 'n', 9, '兵'))
        self.cross62 = ICross(8, 6, 2, 3, None)
        self.cross63 = ICross(9, 6, 1, 3, IPiece('b', 1, 'n', 9, '兵'))


        self.cross64 = ICross(1, 7, 9, 2, None)
        self.cross65 = ICross(2, 7, 8, 2, IPiece('b', 2, 'n', 4, '炮'))
        self.cross66 = ICross(3, 7, 7, 2, None)
        self.cross67 = ICross(4, 7, 6, 2, None)
        self.cross68 = ICross(5, 7, 5, 2, None)
        self.cross69 = ICross(6, 7, 4, 2, None)
        self.cross70 = ICross(7, 7, 3, 2, None)
        self.cross71 = ICross(8, 7, 2, 2, IPiece('b', 2, 'n', 4, '炮'))
        self.cross72 = ICross(9, 7, 1, 2, None)


        self.cross73 = ICross(1, 8, 9, 1, None)
        self.cross74 = ICross(2, 8, 8, 1, None)
        self.cross75 = ICross(3, 8, 7, 1, None)
        self.cross76 = ICross(4, 8, 6, 1, None)
        self.cross77 = ICross(5, 8, 5, 1, None)
        self.cross78 = ICross(6, 8, 4, 1, None)
        self.cross79 = ICross(7, 8, 3, 1, None)
        self.cross80 = ICross(8, 8, 2, 1, None)
        self.cross81 = ICross(9, 8, 1, 1, None)


        self.cross82 = ICross(1, 9, 9, 0, IPiece('b', 1, 'n', 9, '车'))
        self.cross83 = ICross(2, 9, 8, 0, IPiece('b', 3, 'n', 4, '马'))
        self.cross84 = ICross(3, 9, 7, 0, IPiece('b', 4, 'n', 2, '相'))
        self.cross85 = ICross(4, 9, 6, 0, IPiece('b', 5, 'n', 2, '士'))
        self.cross86 = ICross(5, 9, 5, 0, IPiece('b', 6, 'n', 1000, '将'))
        self.cross87 = ICross(6, 9, 4, 0, IPiece('b', 5, 'n', 2, '士'))
        self.cross88 = ICross(7, 9, 3, 0, IPiece('b', 4, 'n', 2, '相'))
        self.cross89 = ICross(8, 9, 2, 0, IPiece('b', 3, 'n', 4, '马'))
        self.cross90 = ICross(9, 9, 1, 0, IPiece('b', 1, 'n', 9, '车'))

