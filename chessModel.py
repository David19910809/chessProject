import numpy as np
import tensorflow as tf
from tensorflow import keras
# 使用暴力破解能解决很多问题，但是不太聪明，教会机器像人一样思考，或许才是人工智能真正的开始
# 暂定使用lstm构建模型
from board import IBoard

# iboard = IBoard()
# boardTarget = np.array(iboard.getnp())
# boardTarget = boardTarget.reshape((10,9))
# print(boardTarget)
# Construct an instance of CustomModel

inputs = keras.Input(shape=(9,50))
x = keras.layers.Dense(900, activation="relu", name="dense_1")(inputs)
x = keras.layers.Dense(900, activation="relu", name="dense_2")(x)
x = keras.layers.Dense(900, activation="relu", name="dense_3")(x)
x = keras.layers.Dense(900, activation="relu", name="dense_4")(x)
outputs = keras.layers.Dense(10, name="predictions")(x)
model = keras.Model(inputs, outputs)
model.compile(optimizer="adam", loss="mse", metrics=["mae"])
# We don't passs a loss or metrics here.
model.summary()
# Just use `fit` as usual -- you can use callbacks, etc.
# Just use `fit` as usual
x = np.arange(4500)
x = x.reshape((50, 10, 9))
x = x.T
x = np.rot90(x,1)
y = np.arange(90)
y = y.reshape((1, 10, 9))
y = y.T
y = np.rot90(y,1)
print(x.shape)
print(y.shape)
print(y)
model.fit(x, y, epochs=3)
model.save('')







