import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


from stn import spatial_transformer_network as transformer
import numpy as np
from PIL import Image
from utils import img2array, array2img
from stn import spatial_transformer_network as transformer
from utils import deg2rad

DIMS = (600, 600)
data_dir = './data/'

# load 4 cat images
img1 = img2array(data_dir + 'cat1.jpg', DIMS, expand=True)#, view=True)
img2 = img2array(data_dir + 'cat2.jpg', DIMS, expand=True)
img3 = img2array(data_dir + 'cat3.jpg', DIMS, expand=True)
img4 = img2array(data_dir + 'cat4.jpg', DIMS, expand=True)

input_img = np.concatenate([img1, img2, img3, img4], axis=0)
B, H, W, C = input_img.shape
print("Input Img Shape: {}".format(input_img.shape))

# initialize affine transform tensor `theta`
degree = 45
theta = np.array([
    [np.cos(deg2rad(degree)), -np.sin(deg2rad(degree)), 0],
    [np.sin(deg2rad(degree)), np.cos(deg2rad(degree)), 0]
])

x = tf.placeholder(tf.float32, [None, H, W, C])

with tf.variable_scope('spatial_transformer'):
    theta = theta.astype('float32')
    theta = theta.flatten()

    # define loc net weight and bias
    loc_in = H * W * C
    loc_out = 6
    W_loc = tf.Variable(tf.zeros([loc_in, loc_out]), name='W_loc')
    b_loc = tf.Variable(initial_value=theta, name='b_loc')

    # tie everything together
    fc_loc = tf.matmul(tf.zeros([B, loc_in]), W_loc) + b_loc
    h_trans = transformer(x, fc_loc)

    # run session
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    y = sess.run(h_trans, feed_dict={x: input_img})
    print("y: {}".format(y.shape))
    array2img(y[0]).show()