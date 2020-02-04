from __future__ import absolute_import  
from __future__ import division  
from __future__ import print_function  
  
import tensorflow as tf  
import numpy as np  
  
w = np.int32(128)
h = np.int32(128)
# 定义权重  
def weight_variable(shape, name):  
    return tf.Variable(tf.truncated_normal(shape, stddev=0.1), name=name)  
# 定义偏差  
def bias_variable(shape, name):  
    return tf.Variable(tf.constant(0.1, shape=shape), name=name)  
# 网络架构  
def model(x, keep_prob):  
      
    x_image = tf.reshape(x, [-1, w, h, 1])  
  
    # Conv1第一层
    with tf.name_scope('conv1'):  
        W_conv1 = weight_variable([3, 3, 1, 16], name="weight")  
        b_conv1 = bias_variable([16], name='bias')
        # 第一层卷积层，输出128*128*16
        h_conv1 = tf.nn.relu(
            tf.nn.conv2d(x_image, W_conv1, strides=[1,1,1,1], padding="SAME", name='conv')  
            + b_conv1)
        # 第一层池化层，输出64*64*16
        h_pool1 = tf.nn.max_pool(h_conv1, ksize=[1,2,2,1], strides=[1,2,2,1],  
                                 padding="SAME", name="pool")
  
    # Conv2第二层
    with tf.name_scope('conv2'):  
        W_conv2 = weight_variable([3, 3, 16, 32], name="weight")  
        b_conv2 = bias_variable([32], name='bias')
        #第二层卷积层，输出64*64*32
        h_conv2 = tf.nn.relu(  
            tf.nn.conv2d(h_pool1, W_conv2, strides=[1,1,1,1], padding="SAME", name='conv')  
            + b_conv2)
        #第二层池化层，输出32*32*32
        h_pool2 = tf.nn.max_pool(h_conv2, ksize=[1,2,2,1], strides=[1,2,2,1],  
                                 padding="SAME", name="pool")  
  
    # fc1 全连接层1
    with tf.name_scope('fc1'):  
        W_fc1 = weight_variable([32*32*32, 256], name="weight")
        b_fc1 = bias_variable([256], name='bias')  
        h_pool2_flat = tf.reshape(h_pool2, [-1, 32*32*32])
        h_fc1 = tf.nn.relu(  
            tf.matmul(h_pool2_flat, W_fc1)+b_fc1)  
  
    # Dropout  随机失活，防止过拟合
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)  
  
    # fc2  全连接层2
    with tf.name_scope('fc2'):  
        W_fc2 = weight_variable([256, 5], name="weight")
        b_fc2 = bias_variable([5], name='bias')
        #softmax分类器
        y = tf.nn.softmax(  
            tf.matmul(h_fc1_drop, W_fc2)+b_fc2, name="output")  
  
    return y  
