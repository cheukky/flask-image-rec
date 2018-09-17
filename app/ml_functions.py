# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import h5py
import os
from app import configs
import sys


# loads saved model
def load_saved_model(path):
    model = keras.models.load_model(path)
    model.compile(optimizer=tf.train.AdamOptimizer(),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model._make_predict_function()
    return model


# upload one image
def parse_image(path):
    img_string = tf.read_file(path)
    img_decoded = tf.image.decode_jpeg(img_string, channels=3)
    img_resized = tf.image.resize_images(img_decoded, [50, 50])
    img = tf.Session().run(img_resized)/255.
    img = np.expand_dims(img, axis=0)
    return img


# predict img
def predict_image(img, model):
    predictions_single = model.predict(img)
    prediction = configs.labels[np.argmax(predictions_single[0])]
    probability = round(100*np.max(predictions_single[0]), 2)

    return prediction, probability, predictions_single[0]


# function to add in more test data
def add_training_data(new_img, new_label, train_img, train_label):
    base_img = np.concatenate((new_img, np.flip(new_img, axis=2)))
    base_label = np.concatenate((new_label, new_label))
    rank, height, width, _ = base_img.shape
    for i in range(1, 3):
        shift_up = np.concatenate((base_img[:, 3*i:, :, :],
                                   np.ones((rank, 3*i, 50, 3))), axis=1)
        shift_down = np.concatenate((np.ones((rank, 3*i, 50, 3)),
                                     base_img[:, :-3*i, :, :]), axis=1)
        shift_left = np.concatenate((base_img[:, :, 3*i:, :],
                                     np.ones((rank, 50, 3*i, 3))), axis=2)
        shift_right = np.concatenate((np.ones((rank, 50, 3*i, 3)),
                                      base_img[:, :, :-3*i, :]), axis=2)
        train_img = np.concatenate((train_img, shift_up, shift_down,
                                    shift_left, shift_right))
        train_label = np.concatenate((train_label, base_label, base_label,
                                      base_label, base_label))
    p = np.random.permutation(len(train_label))
    train_img, train_label = train_img[p], train_label[p]
    return train_img, train_label