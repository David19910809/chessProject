import numpy as np
import copy
from random import choice
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
class IAction:
    def __init__(self,fromCross,toCross):
        self.fromCross = fromCross
        self.toCross = toCross
        self.label = []
        self.name = self.getActionName()

    def getActionName(self):
        action = ''
        str1 = ''
        str2 = ''
        str3 = ''
        str4 = ''
        if self.fromCross.piece.side =='b':
            # action ='黑', self.fromCross.piece.name,'x坐标:',str(self.fromCross.bx),';y坐标',str(self.fromCross.by),'==》x坐标:',str(self.toCross.bx),';y坐标',str(self.toCross.by),self.label

            str1 = self.fromCross.piece.name
            str2 = str(self.fromCross.bx)
            if self.fromCross.by == self.toCross.by:
                str3 = '平'
                str4 = str(self.toCross.bx)
            else:
                if self.fromCross.by < self.toCross.by:
                    str3 = '进'
                    str4 = str(self.toCross.by - self.fromCross.by)
                    if self.fromCross.piece.pieceId == 3 or self.fromCross.piece.pieceId == 4 or self.fromCross.piece.pieceId == 5:
                        str4 = str(self.toCross.bx)
                if self.fromCross.by > self.toCross.by:
                    str3 = '退'
                    str4 = str(self.fromCross.by - self.toCross.by)
                    if self.fromCross.piece.pieceId == 3 or self.fromCross.piece.pieceId == 4 or self.fromCross.piece.pieceId == 5:
                        str4 = str(self.toCross.bx)
            action = str1 + str2 + str3 + str4
        if self.fromCross.piece.side == 'r':
            # action ='红',self.fromCross.piece.name,'x坐标:',str(self.fromCross.rx),';y坐标'+str(self.fromCross.ry),'==》x坐标:',str(self.toCross.rx),';y坐标',str(self.toCross.ry),self.label

            str1 = self.fromCross.piece.name
            str2 = str(self.fromCross.rx)
            if self.fromCross.ry == self.toCross.ry:
                str3 = '平'
                str4 = str(self.toCross.rx)
            else:
                if self.fromCross.ry > self.toCross.ry:
                    str3 = '退'
                    str4 = str(self.fromCross.ry - self.toCross.ry)
                    if self.fromCross.piece.pieceId == 3 or self.fromCross.piece.pieceId == 4 or self.fromCross.piece.pieceId == 5:
                        str4 = str(self.toCross.bx)
                if self.fromCross.ry < self.toCross.ry:
                    str3 = '进'
                    str4 = str(self.toCross.ry - self.fromCross.ry)
                    if self.fromCross.piece.pieceId == 3 or self.fromCross.piece.pieceId == 4 or self.fromCross.piece.pieceId == 5:
                        str4 = str(self.toCross.rx)
            action =  str1 + str2 + str3 + str4
        return action
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
        self.catch_count_r = 0
        self.catch_count_b = 0
        self.unkill_count = 0
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
        self.cross28 = ICross(1, 3, 9, 6, IPiece('r', 7, 'n', 1, '兵'),1)
        self.cross29 = ICross(2, 3, 8, 6, None,1)
        self.cross30 = ICross(3, 3, 7, 6, IPiece('r', 7, 'n', 1, '兵'),1)
        self.cross31 = ICross(4, 3, 6, 6, None,1)
        self.cross32 = ICross(5, 3, 5, 6, IPiece('r', 7, 'n', 1, '兵'),1)
        self.cross33 = ICross(6, 3, 4, 6, None,1)
        self.cross34 = ICross(7, 3, 3, 6, IPiece('r', 7, 'n', 1, '兵'),1)
        self.cross35 = ICross(8, 3, 2, 6, None,1)
        self.cross36 = ICross(9, 3, 1, 6, IPiece('r', 7, 'n', 1, '兵'),1)
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
        self.cross55 = ICross(1, 6, 9, 3, IPiece('b', 7, 'n', 1, '兵'),1)
        self.cross56 = ICross(2, 6, 8, 3, None,1)
        self.cross57 = ICross(3, 6, 7, 3, IPiece('b', 7, 'n', 1, '兵'),1)
        self.cross58 = ICross(4, 6, 6, 3, None,1)
        self.cross59 = ICross(5, 6, 5, 3, IPiece('b', 7, 'n', 1, '兵'),1)
        self.cross60 = ICross(6, 6, 4, 3, None,1)
        self.cross61 = ICross(7, 6, 3, 3, IPiece('b', 7, 'n', 1, '兵'),1)
        self.cross62 = ICross(8, 6, 2, 3, None,1)
        self.cross63 = ICross(9, 6, 1, 3, IPiece('b', 7, 'n', 1, '兵'),1)
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

    #def getAllAction(self):
        #遍历所有子力位置的交叉点，得到所有的行动子集。
        #print('nihao')
        #for cross in self.crosses:
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
    def strQ2B(self,ustring):
        """全角转半角"""
        rstring = ""
        for uchar in ustring:
            inside_code = ord(uchar)
            # print(inside_code)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
                inside_code -= 65248

            rstring += chr(inside_code)
        return rstring
    def getCrossByCoordinate(self,x,y,side):
        if side == 'b':
            for cross in self.crosses:
                if x == cross.bx and y == cross.by:
                    return cross
        if side == 'r':
            for cross in self.crosses:
                if x == cross.rx and y == cross.ry:
                    return cross
        return None

    # 工具方法，根据棋子名称返回交叉点
    def getCrossBypieceId(self, pieceId, side):
        for cross in self.crosses:
            if cross.piece !=None and cross.piece.pieceId == pieceId and cross.piece.side == side:
                return cross

    # 工具方法，根据控制点位列表得到行动列表
    def getActionFromControlList(self,originCross,controlList):
        actionList = []
        for cross in controlList:
            if cross !=None and (cross.piece == None or originCross.piece.side != cross.piece.side):
                actionList.append(IAction(originCross,cross))
        return actionList

    #返回每个棋子的可达交叉点，即控制交叉点
    def getRookControl(self,cross):
        # 车的走法
        controlList = []

        rx = cross.rx
        ry = cross.ry
        while ry < 9:
            controlList.append(self.getCrossByCoordinate(rx,ry+1,'r'))
            if self.getCrossByCoordinate(rx,ry+1,'r').piece != None or ry+1 ==9:
                break
            ry +=1
        ry = cross.ry
        while ry > 0:
            controlList.append(self.getCrossByCoordinate(rx,ry-1,'r'))
            if self.getCrossByCoordinate(rx,ry-1,'r').piece != None or ry-1 ==0:
                break
            ry -=1
        ry = cross.ry
        while rx > 1:
            controlList.append(self.getCrossByCoordinate(rx-1,ry,'r'))
            if self.getCrossByCoordinate(rx-1,ry,'r').piece != None or rx-1 ==1:
                break
            rx -=1
        rx = cross.rx
        while rx < 9:
            controlList.append(self.getCrossByCoordinate(rx+1,ry,'r'))
            if self.getCrossByCoordinate(rx+1,ry,'r').piece != None or rx+1 ==9:
                break
            rx +=1
        return controlList

    def getKnightControl(self, cross):
        # 马的走法
        controlList = []
        rx = cross.rx
        ry = cross.ry
        #马路及控制点
        #(rx-1，ry)(rx，ry+1)(rx+1,ry)(rx,ry-1)
        if self.getCrossByCoordinate(rx - 1, ry, 'r') != None and self.getCrossByCoordinate(rx - 1, ry, 'r').piece == None:
            controlList.append(self.getCrossByCoordinate(rx - 2, ry + 1, 'r'))
            controlList.append(self.getCrossByCoordinate(rx - 2, ry - 1, 'r'))

        if self.getCrossByCoordinate(rx, ry + 1, 'r') != None and self.getCrossByCoordinate(rx, ry + 1, 'r').piece == None:
            controlList.append(self.getCrossByCoordinate(rx + 1, ry + 2, 'r'))
            controlList.append(self.getCrossByCoordinate(rx - 1, ry + 2, 'r'))

        if self.getCrossByCoordinate(rx + 1, ry, 'r') != None and self.getCrossByCoordinate(rx + 1, ry, 'r').piece == None:
            controlList.append(self.getCrossByCoordinate(rx + 2, ry + 1, 'r'))
            controlList.append(self.getCrossByCoordinate(rx + 2, ry - 1, 'r'))

        if self.getCrossByCoordinate(rx, ry - 1, 'r') != None and self.getCrossByCoordinate(rx, ry - 1, 'r').piece == None:
            controlList.append(self.getCrossByCoordinate(rx + 1, ry - 2, 'r'))
            controlList.append(self.getCrossByCoordinate(rx - 1, ry - 2, 'r'))

        return controlList

    def getCannonControl(self, cross):
        # 炮的控制点
        controlList = []
        rx = cross.rx
        ry = cross.ry
        flag = 'N'
        while ry < 9:
            if flag == 'Y' :
                controlList.append(self.getCrossByCoordinate(rx, ry + 1, 'r'))
                if self.getCrossByCoordinate(rx, ry + 1, 'r').piece != None:
                    break
            if self.getCrossByCoordinate(rx, ry + 1, 'r').piece != None:
                flag = 'Y'
            ry += 1
        ry = cross.ry
        flag = 'N'
        while ry > 0:
            if flag == 'Y':
                controlList.append(self.getCrossByCoordinate(rx, ry - 1, 'r'))
                if self.getCrossByCoordinate(rx, ry - 1, 'r').piece != None:
                    break
            if self.getCrossByCoordinate(rx, ry - 1, 'r').piece != None:
                flag = 'Y'
            ry -= 1
        ry = cross.ry
        flag = 'N'
        while rx > 1:
            if flag == 'Y':
                controlList.append(self.getCrossByCoordinate(rx - 1, ry, 'r'))
                if self.getCrossByCoordinate(rx - 1, ry , 'r').piece != None:
                    break
            if self.getCrossByCoordinate(rx - 1, ry, 'r').piece != None:
                flag = 'Y'
            rx -= 1
        rx = cross.rx
        flag = 'N'
        while rx < 9:
            if flag == 'Y':
                controlList.append(self.getCrossByCoordinate(rx + 1, ry, 'r'))
                if self.getCrossByCoordinate(rx + 1, ry, 'r').piece != None:
                    break
            if self.getCrossByCoordinate(rx + 1, ry, 'r').piece != None:
                flag = 'Y'
            rx += 1
        return controlList

    def getCannonAccess(self, cross):
        controlList = []

        rx = cross.rx
        ry = cross.ry
        while ry < 9:
            if self.getCrossByCoordinate(rx, ry + 1, 'r').piece != None or ry + 1 == 10:
                break
            controlList.append(self.getCrossByCoordinate(rx, ry + 1, 'r'))
            ry += 1
        ry = cross.ry
        while ry > 0:
            if self.getCrossByCoordinate(rx, ry - 1, 'r').piece != None or ry - 1 == -1:
                break
            controlList.append(self.getCrossByCoordinate(rx, ry - 1, 'r'))
            ry -= 1
        ry = cross.ry
        while rx > 1:
            if self.getCrossByCoordinate(rx - 1, ry, 'r').piece != None or rx - 1 == 0:
                break
            controlList.append(self.getCrossByCoordinate(rx - 1, ry, 'r'))
            rx -= 1
        rx = cross.rx
        while rx < 9:
            if self.getCrossByCoordinate(rx + 1, ry, 'r').piece != None or rx + 1 == 10:
                break
            controlList.append(self.getCrossByCoordinate(rx + 1, ry, 'r'))
            rx += 1
        return controlList

    def getPawnControl(self, cross):
        controlList = []
        rx = cross.rx
        ry = cross.ry
        bx = cross.bx
        by = cross.by
        if cross.piece.side == 'r' :
            if ry <= 4:
                controlList.append(self.getCrossByCoordinate(rx, ry + 1, 'r'))
            else:
                controlList.append(self.getCrossByCoordinate(rx, ry + 1, 'r'))
                controlList.append(self.getCrossByCoordinate(rx - 1, ry, 'r'))
                controlList.append(self.getCrossByCoordinate(rx + 1, ry, 'r'))
        else:
            if by <= 4:
                controlList.append(self.getCrossByCoordinate(bx, by + 1, 'b'))
            else:
                controlList.append(self.getCrossByCoordinate(bx, by + 1, 'b'))
                controlList.append(self.getCrossByCoordinate(bx - 1, by, 'b'))
                controlList.append(self.getCrossByCoordinate(bx + 1, by, 'b'))

        return controlList

    def getBishopControl(self, cross):
        controlList = []
        rx = cross.rx
        ry = cross.ry
        bx = cross.bx
        by = cross.by
        if cross.piece.side == 'b':
            if self.getCrossByCoordinate(bx - 1, by + 1, 'b')!=None and self.getCrossByCoordinate(bx - 1, by + 1, 'b').piece == None  and by + 2 <= 4 :
                controlList.append(self.getCrossByCoordinate(bx - 2, by + 2, 'b'))
            if self.getCrossByCoordinate(bx - 1, by - 1, 'b') !=None and self.getCrossByCoordinate(bx - 1, by - 1, 'b').piece == None :
                controlList.append(self.getCrossByCoordinate(bx - 2, by - 2, 'b'))
            if self.getCrossByCoordinate(bx + 1, by + 1, 'b')!= None and self.getCrossByCoordinate(bx + 1, by + 1, 'b').piece == None and by + 2 <= 4:
                controlList.append(self.getCrossByCoordinate(bx + 2, by + 2, 'b'))
            if self.getCrossByCoordinate(bx + 1, by - 1, 'b')!= None and self.getCrossByCoordinate(bx + 1, by - 1, 'b').piece == None :
                controlList.append(self.getCrossByCoordinate(bx + 2, by - 2, 'b'))
        else:
            if self.getCrossByCoordinate(rx - 1, ry + 1, 'r') != None and self.getCrossByCoordinate(rx - 1, ry + 1, 'r').piece == None and ry + 2 <= 4 :
                controlList.append(self.getCrossByCoordinate(rx - 2, ry + 2, 'r'))
            if self.getCrossByCoordinate(rx - 1, ry - 1, 'r') != None and self.getCrossByCoordinate(rx - 1, ry - 1, 'r').piece == None :
                controlList.append(self.getCrossByCoordinate(rx - 2, ry - 2, 'r'))
            if self.getCrossByCoordinate(rx + 1, ry + 1, 'r') != None and self.getCrossByCoordinate(rx + 1, ry + 1, 'r').piece == None and ry + 2 <= 4:
                controlList.append(self.getCrossByCoordinate(rx + 2, ry + 2, 'r'))
            if self.getCrossByCoordinate(rx + 1, ry - 1, 'r') != None and self.getCrossByCoordinate(rx + 1, ry - 1, 'r').piece == None :
                controlList.append(self.getCrossByCoordinate(rx + 2, ry - 2, 'r'))

        return controlList

    def getOfficialControl(self, cross):
        controlList = []
        rx = cross.rx
        ry = cross.ry
        bx = cross.bx
        by = cross.by
        if cross.piece.side == 'b':
            if by == 0 or by == 2:
                controlList.append(self.getCrossByCoordinate(5, 1, 'b'))
            else:
                controlList.append(self.getCrossByCoordinate(4, 0, 'b'))
                controlList.append(self.getCrossByCoordinate(6, 0, 'b'))
                controlList.append(self.getCrossByCoordinate(6, 2, 'b'))
                controlList.append(self.getCrossByCoordinate(4, 2, 'b'))
        else:
            if ry == 0 or ry == 2:
                controlList.append(self.getCrossByCoordinate(5, 1, 'r'))
            else:
                controlList.append(self.getCrossByCoordinate(4, 0, 'r'))
                controlList.append(self.getCrossByCoordinate(6, 0, 'r'))
                controlList.append(self.getCrossByCoordinate(6, 2, 'r'))
                controlList.append(self.getCrossByCoordinate(4, 2, 'r'))
        return controlList

    def getKingControl(self, cross):
        controlList = []
        rx = cross.rx
        ry = cross.ry
        bx = cross.bx
        by = cross.by
        if cross.piece.side == 'r' :
            if rx - 1 >= 4 :
                controlList.append(self.getCrossByCoordinate(rx - 1, ry, 'r'))
            if rx + 1 <= 6 :
                controlList.append(self.getCrossByCoordinate(rx + 1, ry, 'r'))
            if ry - 1 >= 0 :
                controlList.append(self.getCrossByCoordinate(rx, ry - 1, 'r'))
            if ry + 1 <= 2 :
                controlList.append(self.getCrossByCoordinate(rx, ry + 1, 'r'))
        else:
            if bx - 1 >= 4 :
                controlList.append(self.getCrossByCoordinate(bx - 1, by, 'b'))
            if bx + 1 <= 6 :
                controlList.append(self.getCrossByCoordinate(bx + 1, by, 'b'))
            if by - 1 >= 0 :
                controlList.append(self.getCrossByCoordinate(bx, by - 1, 'b'))
            if by + 1 <= 2 :
                controlList.append(self.getCrossByCoordinate(bx, by + 1, 'b'))
        return controlList

    #根据棋子返回控制列表
    def getPieceControl(self,cross):
        if cross.piece.pieceId == 1:
            return self.getRookControl(cross)
        if cross.piece.pieceId == 2:
            return self.getCannonControl( cross)
        if cross.piece.pieceId == 3:
            return self.getKnightControl( cross)

    # 获取总的控制点位
    def controlList(self, side):
        controlList = []
        for cross in self.crosses:
            if cross.piece != None and cross.piece.side == side:
                if cross.piece.pieceId == 2:
                    controlList.extend(self.getCannonControl(cross))
                if cross.piece.pieceId == 1:
                    controlList.extend(self.getRookControl(cross))
                if cross.piece.pieceId == 3:
                    controlList.extend(self.getKnightControl(cross))
                if cross.piece.pieceId == 4:
                    controlList.extend(self.getBishopControl(cross))
                if cross.piece.pieceId == 5:
                    controlList.extend(self.getOfficialControl(cross))
                if cross.piece.pieceId == 6:
                    controlList.extend(self.getKingControl(cross))
                if cross.piece.pieceId == 7:
                    controlList.extend(self.getPawnControl(cross))
        return controlList
    #获取行动列表
    def chessAction(self):
        actionList = []
        valideActionList = []
        valideActionList_final = []
        for cross in self.crosses:
            if cross.piece != None and cross.piece.side == self.player:
                if cross.piece.pieceId == 2:
                    controlList = self.getCannonControl(cross)
                    accessList = self.getCannonAccess(cross)
                    for controlCross in controlList:
                        if controlCross.piece !=None:
                            accessList.append(controlCross)
                    actionList.extend(self.getActionFromControlList(cross,accessList))
                if cross.piece.pieceId == 1:
                    actionList.extend(self.getActionFromControlList(cross,self.getRookControl(cross)))
                if cross.piece.pieceId == 3:
                    actionList.extend(self.getActionFromControlList(cross,self.getKnightControl(cross)))
                if cross.piece.pieceId == 4:
                    actionList.extend(self.getActionFromControlList(cross,self.getBishopControl(cross)))
                if cross.piece.pieceId == 5:
                    actionList.extend(self.getActionFromControlList(cross,self.getOfficialControl(cross)))
                if cross.piece.pieceId == 6:
                    actionList.extend(self.getActionFromControlList(cross,self.getKingControl(cross)))
                if cross.piece.pieceId == 7:
                    actionList.extend(self.getActionFromControlList(cross,self.getPawnControl(cross)))
        #保护老帅意识
        if self.player == 'b':
            otherSide = 'r'
        else:
            otherSide = 'b'

        for action in actionList:
            isValide = 'valide'
            actionName = action.getActionName()
            #先在棋盘完成行动
            toCross_tmp = copy.deepcopy(action.toCross.piece)
            fromCross_tmp = copy.deepcopy(action.fromCross.piece)
            action.toCross.piece = action.fromCross.piece
            action.fromCross.piece = None
            #获取对方控制点位列表，如果老帅被控制，则判定行动非法
            controlList_otherSide = self.controlList(otherSide)
            for otherSideCross in controlList_otherSide:
                if otherSideCross != None and otherSideCross.piece != None and otherSideCross.piece.pieceId == 6 and otherSideCross.piece.side == self.player:
                    #行动不可让老帅被将军
                    #print('行动非法',actionName)
                    action.toCross.piece = copy.deepcopy(toCross_tmp)
                    action.fromCross.piece = copy.deepcopy(fromCross_tmp)
                    isValide = 'unValide'
                    break
            #老帅照面限制
            if  isValide != 'unValide':
                king1 = self.getCrossBypieceId(6,'r')
                king2 = self.getCrossBypieceId(6,'b')
                ryflag1 = king1.ry
                ryflag2 = king2.ry
                ryline = 'N'
                while ryflag2 - ryflag1 >0:
                    if self.getCrossByCoordinate(king1.rx,ryflag1+1,'r') != None and self.getCrossByCoordinate(king1.rx,ryflag1+1,'r').piece != None:
                        ryline = 'Y'
                        break
                    ryflag1+=1
                if king1.rx == king2.rx and ryline == 'N':
                    isValide = 'unValide'
                    #print('!!!非法行动', actionName)
            if isValide == 'valide':
                valideActionList.append(action)
            action.toCross.piece = copy.deepcopy(toCross_tmp)
            action.fromCross.piece = copy.deepcopy(fromCross_tmp)
        #行动标签
        for action in valideActionList:
            toCross_tmp = copy.deepcopy(action.toCross.piece)
            fromCross_tmp = copy.deepcopy(action.fromCross.piece)
            action.toCross.piece = action.fromCross.piece
            action.fromCross.piece = None
            piececontrolList = self.getPieceControl(action.toCross)
            controlList = self.controlList(fromCross_tmp.side)
            controlList_otherSide = self.controlList(otherSide)
            #吃子
            if toCross_tmp!=None :
                action.label.append('eat')
            # 捉子
            if piececontrolList != None:
                for controlCross in piececontrolList:
                    if controlCross != None and controlCross.piece != None and controlCross.piece.side != fromCross_tmp.side:
                        flag = 'Y'
                        for otherSideControlCross in controlList_otherSide:
                            if controlCross == otherSideControlCross:
                                flag = 'N'
                                break
                        if flag == 'Y':
                            action.label.append('catch')
                            break
            #将军
            for cross in controlList:
                if cross != None and cross.piece != None and cross.piece.pieceId == 6 and self.player != cross.piece.side:
                    action.label.append('check')
            action.toCross.piece = copy.deepcopy(toCross_tmp)
            action.fromCross.piece = copy.deepcopy(fromCross_tmp)
        #长捉限定
        for action in valideActionList:
            if self.player == 'b' and (self.catch_count_b < 8 or ('catch' not in action.label or 'check' not in action.label)):
                valideActionList_final.append(action)
            if self.player == 'r' and (self.catch_count_r < 8 or ('catch' not in action.label or 'check' not in action.label)):
                valideActionList_final.append(action)
        return   valideActionList_final



    def takeAction(self,actionName):
        actionList = self.chessAction()
        if actionList ==None or len(actionList) <1:
            return self.player+'输'
        if self.unkill_count >= 121:
            return '和'
        else:
            actionTaken = None
            for action in actionList:
                if self.strQ2B(action.getActionName()) == self.strQ2B(actionName):
                    actionTaken = action
            print(actionTaken.getActionName(), actionTaken.label)
            actionTaken.toCross.piece = actionTaken.fromCross.piece
            actionTaken.fromCross.piece = None
            if self.player == 'r':
                self.player = 'b'
            else:
                self.player = 'r'
            if 'catch' in actionTaken.label or 'check' in actionTaken.label:
                self.catch_count_b += 1
            else:
                self.catch_count_b = 0
            if 'eat' not in actionTaken.label:
                self.unkill_count += 1
            else:
                self.unkill_count = 0
        mat = "{strtmp: ^{len}}"
        for cross in myboard.crosses:
            if (cross.rx % 9 == 0):
                if (cross.piece != None):
                    strtmp = cross.piece.name
                    if cross.piece.side == 'r':
                        print("\033[0;37;41m" + mat.format(strtmp=strtmp, len=5) + "\033[0m")
                    else:
                        print("\033[0;37;43m" + mat.format(strtmp=strtmp, len=5) + "\033[0m")
                else:
                    strtmp = "口"
                    print(mat.format(strtmp=strtmp,len=5))
            else:
                if (cross.piece != None):
                    strtmp = cross.piece.name
                    if cross.piece.side == 'r':
                        print("\033[0;37;41m"+mat.format(strtmp=strtmp,len=5)+"\033[0m", end="")
                    else:
                        print("\033[0;37;43m" + mat.format(strtmp=strtmp, len=5) + "\033[0m", end="")
                else:
                    strtmp = "口"
                    print(mat.format(strtmp=strtmp, len=5), end="")

    def getNp(self):
        crossList = []
        for cross in self.crosses:
            if (cross.piece != None):
                if cross.piece.side == 'r':
                    crossList.append(cross.piece.pieceId)
                else:
                    crossList.append(-cross.piece.pieceId)
            else:
                crossList.append(0)
        return crossList

    def getNpList(self):
        boardList = []
        valideActionList_final = self.chessAction()
        for action in valideActionList_final:
            # 先在棋盘完成行动
            toCross_tmp = copy.deepcopy(action.toCross.piece)
            fromCross_tmp = copy.deepcopy(action.fromCross.piece)

            crossList = []
            for cross in self.crosses:
                if (cross.piece != None):
                    if cross.piece.side == 'r':
                        crossList.append(cross.piece.pieceId)
                    else:
                        crossList.append(-cross.piece.pieceId)
                else:
                    crossList.append(0)
            crossList_tmp = copy.deepcopy(crossList)
            boardList.append(crossList_tmp)
            crossList.clear()
            action.toCross.piece = copy.deepcopy(toCross_tmp)
            action.fromCross.piece = copy.deepcopy(fromCross_tmp)
        if len(boardList)<50:
            while 50 - len(boardList) > 0:
                boardList.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

        return boardList

    def printBoard(self,y):
        # y = np.array([0.1,0.5,0.8,-0.4,1.1,1.8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        # y = self.getNp()
        # y = np.array(y)
        # y = y.reshape((1, 10, 9))
        # y = y.T
        # y = np.rot90(y,1)
       #########################
        y = np.rot90(y, -1)
        y = y.T
        y = y.reshape((90))
        y = np.asarray(y)
        y = np.rint(y)
        #print(y)

        mat = "{strtmp: ^{len}}"
        flag = 1
        for i in y:
            if (flag % 9 == 0):
                if (i == 1):
                    print("\033[0;37;41m" + mat.format(strtmp='车', len=5) + "\033[0m")
                if (i == 2):
                    print("\033[0;37;41m" + mat.format(strtmp='炮', len=5) + "\033[0m")
                if (i == 3):
                    print("\033[0;37;41m" + mat.format(strtmp='马', len=5) + "\033[0m")
                if (i == 4):
                    print("\033[0;37;41m" + mat.format(strtmp='相', len=5) + "\033[0m")
                if (i == 5):
                    print("\033[0;37;41m" + mat.format(strtmp='士', len=5) + "\033[0m")
                if (i == 6):
                    print("\033[0;37;41m" + mat.format(strtmp='将', len=5) + "\033[0m")
                if (i == 7):
                    print("\033[0;37;41m" + mat.format(strtmp='兵', len=5) + "\033[0m")
                if (i == -1):
                    print("\033[0;37;43m" + mat.format(strtmp='车', len=5) + "\033[0m")
                if (i == -2):
                    print("\033[0;37;43m" + mat.format(strtmp='炮', len=5) + "\033[0m")
                if (i == -3):
                    print("\033[0;37;43m" + mat.format(strtmp='马', len=5) + "\033[0m")
                if (i == -4):
                    print("\033[0;37;43m" + mat.format(strtmp='相', len=5) + "\033[0m")
                if (i == -5):
                    print("\033[0;37;43m" + mat.format(strtmp='士', len=5) + "\033[0m")
                if (i == -6):
                    print("\033[0;37;43m" + mat.format(strtmp='将', len=5) + "\033[0m")
                if (i == -7):
                    print("\033[0;37;43m" + mat.format(strtmp='兵', len=5) + "\033[0m")
                if (i == 0):
                    print( mat.format(strtmp='口', len=5))
            else:
                if (i == 1):
                    print("\033[0;37;41m" + mat.format(strtmp='车', len=5) + "\033[0m",end = "")
                if (i == 2):
                    print("\033[0;37;41m" + mat.format(strtmp='炮', len=5) + "\033[0m",end = "")
                if (i == 3):
                    print("\033[0;37;41m" + mat.format(strtmp='马', len=5) + "\033[0m",end = "")
                if (i == 4):
                    print("\033[0;37;41m" + mat.format(strtmp='相', len=5) + "\033[0m",end = "")
                if (i == 5):
                    print("\033[0;37;41m" + mat.format(strtmp='士', len=5) + "\033[0m",end = "")
                if (i == 6):
                    print("\033[0;37;41m" + mat.format(strtmp='将', len=5) + "\033[0m",end = "")
                if (i == 7):
                    print("\033[0;37;41m" + mat.format(strtmp='兵', len=5) + "\033[0m",end = "")
                if (i == -1):
                    print("\033[0;37;43m" + mat.format(strtmp='车', len=5) + "\033[0m",end = "")
                if (i == -2):
                    print("\033[0;37;43m" + mat.format(strtmp='炮', len=5) + "\033[0m",end = "")
                if (i == -3):
                    print("\033[0;37;43m" + mat.format(strtmp='马', len=5) + "\033[0m",end = "")
                if (i == -4):
                    print("\033[0;37;43m" + mat.format(strtmp='相', len=5) + "\033[0m",end = "")
                if (i == -5):
                    print("\033[0;37;43m" + mat.format(strtmp='士', len=5) + "\033[0m",end = "")
                if (i == -6):
                    print("\033[0;37;43m" + mat.format(strtmp='将', len=5) + "\033[0m",end = "")
                if (i == -7):
                    print("\033[0;37;43m" + mat.format(strtmp='兵', len=5) + "\033[0m",end = "")
                if (i == 0):
                    print(mat.format(strtmp='口', len=5),end = "")
            flag += 1



if __name__ == '__main__':
    myboard = IBoard()
    myboard.takeAction('炮2平5')










