#!/usr/bin/env python
# coding: utf-8

# # Chapter 2:	Densely Connected Networks

import keras
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg
from keras.datasets import mnist
from keras.layers import *
from keras.models import *
from keras.optimizers import sgd
from keras.utils import to_categorical

# Save the files manually in ~/.keras/datasets/ as MN cannot download from
# Internet
(x_train, y_train), (x_test, y_test) = mnist.load_data()

np.set_printoptions(precision=2, suppress=True, linewidth=120)

x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# print(x_test.shape)
# (10000, 28, 28)

x_train = x_train.reshape(60000, 28, 28, 1)
x_test = x_test.reshape(10000, 28, 28, 1)

y_train = to_categorical(y_train, num_classes=10)
y_test = to_categorical(y_test, num_classes=10)

# Build the model

model = Sequential()
model.add(Conv2D(32, (5, 5), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(10, activation='softmax'))

model.summary()
#exit(1)

#
# Definition, training and evaluation
#

batch_size = 50
num_classes = 10
#epochs=50
epochs=50

model.compile(loss='categorical_crossentropy',
			  optimizer='sgd',
			  metrics=['accuracy'])

model.fit(x_train, y_train,
		  batch_size=batch_size,
		  epochs=epochs,
		  verbose=1)

test_loss, test_acc = model.evaluate(x_test, y_test)

print('Test loss:', test_loss)
print('Test accuracy:', test_acc)

# Predictions

predictions = model.predict(x_test)
print(predictions[11])
np.sum(predictions[11])
np.argmax(predictions[11])

# Look at confusion matrix 
# Note, this code is taken straight from the SKLEARN website, an nice way of
# viewing confusion matrix.

def plot_confusion_matrix(cm, classes,
						  normalize=False,
						  title='Confusion matrix',
						  cmap=plt.cm.Blues):
	"""
	This function prints and plots the confusion matrix.
	Normalization can be applied by setting `normalize=True`.
	"""
	plt.imshow(cm, interpolation='nearest', cmap=cmap)
	plt.title(title)
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=45)
	plt.yticks(tick_marks, classes)

	if normalize:
		cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

	thresh = cm.max() / 2.
	for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
		plt.text(j, i, cm[i, j],
				 horizontalalignment="center",
				 color="white" if cm[i, j] > thresh else "black")

	plt.tight_layout()
	plt.ylabel('Actual class')
	plt.xlabel('Predicted class')


from collections import Counter
from sklearn.metrics import confusion_matrix
import itertools

# Predict the values from the validation dataset
Y_pred = model.predict(x_test)
# Convert predictions classes to one hot vectors
Y_pred_classes = np.argmax(Y_pred, axis = 1)
# Convert validation observations to one hot vectors
Y_true = np.argmax(y_test, axis = 1)
# compute the confusion matrix
confusion_mtx = confusion_matrix(Y_true, Y_pred_classes)
# plot the confusion matrix
plot_confusion_matrix(confusion_mtx, classes = range(10))
plt.savefig("plot.png")
