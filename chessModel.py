import numpy as np
import tensorflow as tf
from tensorflow import keras
#使用暴力破解能解决很多问题，但是不太聪明，教会机器像人一样思考，或许才是人工智能真正的开始
#暂定使用lstm构建模型
from board import IBoard

# iboard = IBoard()
# boardTarget = np.array(iboard.getnp())
# boardTarget = boardTarget.reshape((10,9))
# print(boardTarget)
# Construct an instance of CustomModel

inputs = keras.Input(shape=(9,2))
inputs = keras.layers.Dense(900,activation="relu")(inputs)
outputs = keras.layers.Dense(900,activation="relu")(inputs)
# inputs = keras.layers.Dense(2)(inputs)
# inputs = keras.layers.Dense(3)(inputs)
# inputs = keras.layers.Dense(4)(inputs)
# inputs = keras.layers.Dense(5)(inputs)
# inputs = keras.layers.Dense(6)(inputs)
# inputs = keras.layers.Dense(7)(inputs)
# inputs = keras.layers.Dense(8)(inputs)
# inputs = keras.layers.Dense(9)(inputs)
# inputs = keras.layers.Dense(10)(inputs)
# inputs = keras.layers.Dense(11)(inputs)
# inputs = keras.layers.Dense(12)(inputs)
# outputs = keras.layers.Dense(13)(inputs)
model = keras.Model(inputs, outputs)

# We don't passs a loss or metrics here.
model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# Just use `fit` as usual -- you can use callbacks, etc.
# Just use `fit` as usual
x =  np.arange(180)
x = x.reshape((10,9,2))
x = x.reshape((10,9,2))
y = np.arange(90)
y = y.reshape((10, 9, 1))
print('##########')
print(x)
print('##########')
print(y)
model.fit(x, y, epochs=3)
print('##########')
y = y.reshape((1, 10, 9))
print(y)






