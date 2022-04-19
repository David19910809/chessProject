import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
from datetime import datetime
from board import IBoard
from actionReader import actionReader
from keras.models import load_model
model = load_model('C://model')
test = IBoard()
test.takeAction('炮2平5')
test.takeAction('炮2平5')
# test.takeAction('炮2平5')
x = test.getNpList()
x = np.array(x)
x = x.reshape((1, 4500))
x = x.reshape((50, 10, 9))
x = x.T
x = np.rot90(x,1)
y = model(x)
test.printBoard(y)
y = np.rot90(y, -1)
y = y.T
y = np.rint(y)

print(y)