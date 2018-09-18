# TensorFlow and tf.keras
import tensorflow as tf

# Helper libraries
import os
import numpy as np
import matplotlib as mpl
from app import configs

if os.environ.get('DISPLAY', '') == '':
    mpl.use('Agg')
import matplotlib.pyplot as plt


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


def save_value_array(predictions_array, filename):
    predictions_array = predictions_array
    plt.clf()
    plt.grid(False)
    plt.xticks(range(1, 12), configs.labels[1:] , rotation=90)
    plt.yticks([])
    thisplot = plt.bar(range(1, 12), predictions_array[1:], color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array[1:])

    thisplot[predicted_label].set_color('blue')
    plt.savefig('data/uploads/plot_' + filename,
                bbox_inches='tight', format='jpg')


# function to add in more test data
def add_training_data(new_img, new_label, train_img, train_label):
    base_img = np.concatenate((new_img, np.flip(new_img, axis=2)))
    base_label = np.concatenate(([new_label], [new_label]))
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


def train_model(model, train_img, train_label):
    model.fit(train_img, train_label, epochs=10)
    return model
