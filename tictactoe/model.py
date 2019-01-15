import tensorflow as tf
import os

model_path = "model.h5"


def get_model():
    if os.path.exists(model_path):
        return tf.keras.models.load_model(model_path)
    else:
        model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(9, )),
            tf.keras.layers.Dense(64, activation=tf.nn.relu),
            tf.keras.layers.Dense(64, activation=tf.nn.relu),
            tf.keras.layers.Dense(9, activation=tf.nn.softmax)
        ])

        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        return model


def save_model(model):
    model.save(model_path)