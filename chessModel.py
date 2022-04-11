import numpy as np
import tensorflow as tf
from tensorflow import keras
#使用暴力破解能解决很多问题，但是不太聪明，教会机器像人一样思考，或许才是人工智能真正的开始
#暂定使用lstm构建模型
from board import IBoard

iboard = IBoard()
# Construct an instance of CustomModel
inputs = keras.Input(iboard.crosses)
outputs = keras.layers.Dense(1)(inputs)
model = keras.Model(inputs, outputs)

# We don't passs a loss or metrics here.
model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# Just use `fit` as usual -- you can use callbacks, etc.
xtest = np.random.random((1000,90))
ytest = np.random.random((1000,1))
model.fit(xtest, ytest, epochs=5)


