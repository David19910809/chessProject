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
    def __init__(self,side,pieceId,isDead,value):
        self.side = side
        self.pieceId = pieceId
        self.isDead = isDead
        self.value = value


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
        self.cross1 = new ICross(1,0,9,10)