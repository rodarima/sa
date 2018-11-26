#!/usr/bin/env python
# coding: utf-8

# # Chapter 2:	Densely Connected Networks

from keras.datasets import mnist
from keras.layers import *
from keras.models import *
from keras.utils import to_categorical

# Save the files manually in ~/.keras/datasets/ as MN cannot download from
# Internet
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# print(x_test.shape)
# (10000, 28, 28)

x_train = x_train.reshape(60000, 28, 28, 1)
x_test = x_test.reshape(10000, 28, 28, 1)

y_train = to_categorical(y_train, num_classes=10)
y_test = to_categorical(y_test, num_classes=10)

# Build the model

#model = Sequential()
#model.add(Conv2D(32, (5, 5), activation='relu', input_shape=(28, 28, 1)))
#model.add(MaxPooling2D((2, 2)))
#model.add(Flatten())
#model.add(Dense(10, activation='softmax'))


model = Sequential()
model.add(Conv2D(32, (5, 5), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (5, 5), activation='relu'))
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
epochs=50
#epochs=2

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



#Serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as f:
	f.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

