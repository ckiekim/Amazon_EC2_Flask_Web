from tabnanny import verbose
import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

seed = 2022
np.random.seed(seed)
tf.random.set_seed(seed)
(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
X_train = X_train.reshape(-1, 28, 28, 1) / 255.
X_test = X_test.reshape(-1, 28, 28, 1) / 255.
Y_train = to_categorical(y_train)
Y_test = to_categorical(y_test)

model = Sequential([
    Conv2D(32, kernel_size=(3,3), input_shape=(28,28,1), activation='relu'),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(),
    Dropout(0.25),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')
])
model.compile('adam', 'categorical_crossentropy', ['accuracy'])
model_path = '../static/model/fashion_mnist_cnn.h5'
mc = ModelCheckpoint(model_path, save_best_only=True, verbose=1)
es = EarlyStopping(patience=10)

hist = model.fit(
    X_train, Y_train, validation_split=0.2, epochs=100, batch_size=200, verbose=0,
    callbacks=[mc, es]
)

best_model = load_model(model_path)
print(best_model.evaluate(X_test, Y_test, verbose=0))
