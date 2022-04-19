import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
from datetime import datetime
from board import IBoard
from actionReader import actionReader
# iboard = IBoard()
# boardTarget = np.array(iboard.getnp())
# boardTarget = boardTarget.reshape((10,9))
# print(boardTarget)
# Construct an instance of CustomModel
def strQ2B(ustring):
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
#神经网络
inputs = keras.Input(shape=(9,50))
x = keras.layers.Dense(4500, activation="relu", name="dense_1")(inputs)
x = keras.layers.Dense(2250, activation="relu", name="dense_2")(x)
x = keras.layers.Dense(900, activation="relu", name="dense_3")(x)
x = keras.layers.Dense(450, activation="relu", name="dense_4")(x)
x = keras.layers.Dense(180, activation="relu", name="dense_5")(x)
outputs = keras.layers.Dense(1, name="predictions")(x)
model = keras.Model(inputs, outputs)
model.compile(optimizer="adam", loss="mse", metrics=["mae"])
# We don't passs a loss or metrics here.
#模型结构预览
model.summary()
# Just use `fit` as usual -- you can use callbacks, etc.
# Just use `fit` as usual
#模拟测试数据
# y = np.arange(90)
# x = np.arange(4500)
# y = y.reshape((1, 10, 9))
# x = x.reshape((50, 10, 9))
#矩阵转置 旋转
# x = x.T
# x = np.rot90(x,1)
# y = y.T
# y = np.rot90(y,1)
# print(x.shape)
# print(y.shape)
#iboard = IBoard()
actionReader = actionReader()
timeEnd = datetime(2022, 4, 21, 18, 18, 1, 186250)
for filename in os.listdir(r'C://Users//user1//Desktop//all'):
    time = datetime.now()
    print(time > timeEnd)
    if time>timeEnd:
        break
    file = open('C://Users//user1//Desktop//all//'+filename)
    actionList = actionReader.getActionList(file)
    iboard = IBoard()
    for action in actionList:
        try:
            x = iboard.getNpList()
            x = np.array(x)
            x = x.reshape((1, 4500))
            x = x.reshape((50, 10, 9))

        except ValueError:
            break
        boardChessActionList = iboard.chessAction()
        flag = 'false'
        for boardAction in boardChessActionList:
            if strQ2B(boardAction.getActionName()) == strQ2B(action):
                flag = 'true'
        if flag == 'false':
            break
        iboard.takeAction(action)
        y = iboard.getNp()
        y = np.array(y)
        y = y.reshape((1, 10, 9))
        # 棋盘矩阵转置 旋转
        x = x.T
        x = np.rot90(x,1)
        y = y.T
        y = np.rot90(y,1)
        model.fit(x, y, epochs=10)
#训练模型

model.save('C://model', overwrite=True, include_optimizer=True )








