import numpy as np
import tensorflow as tf
from tensorflow import keras
from board import IBoard

# iboard = IBoard()
# boardTarget = np.array(iboard.getnp())
# boardTarget = boardTarget.reshape((10,9))
# print(boardTarget)
# Construct an instance of CustomModel
#神经网络
inputs = keras.Input(shape=(9,50))
x = keras.layers.Dense(900, activation="relu", name="dense_1")(inputs)
x = keras.layers.Dense(900, activation="relu", name="dense_2")(x)
x = keras.layers.Dense(900, activation="relu", name="dense_3")(x)
x = keras.layers.Dense(900, activation="relu", name="dense_4")(x)
x = keras.layers.Dense(900, activation="relu", name="dense_5")(x)
x = keras.layers.Dense(900, activation="relu", name="dense_6")(x)
x = keras.layers.Dense(900, activation="relu", name="dense_7")(x)
x = keras.layers.Dense(900, activation="relu", name="dense_8")(x)
x = keras.layers.Dense(900, activation="relu", name="dense_9")(x)
x = keras.layers.Dense(900, activation="relu", name="dense_10")(x)
x = keras.layers.Dense(900, activation="relu", name="dense_11")(x)
x = keras.layers.Dense(900, activation="relu", name="dense_12")(x)
x = keras.layers.Dense(900, activation="relu", name="dense_13")(x)
outputs = keras.layers.Dense(10, name="predictions")(x)
model = keras.Model(inputs, outputs)
model.compile(optimizer="adam", loss="mse", metrics=["mae"])
# We don't passs a loss or metrics here.
#模型结构预览
model.summary()
# Just use `fit` as usual -- you can use callbacks, etc.
# Just use `fit` as usual
#模拟测试数据
y = np.arange(90)
x = np.arange(4500)
y = y.reshape((1, 10, 9))
x = x.reshape((50, 10, 9))
#矩阵转置 旋转
x = x.T
x = np.rot90(x,1)
y = y.T
y = np.rot90(y,1)
print(x.shape)
print(y.shape)
#训练模型
model.fit(x, y, epochs=3)
# model.save('')







