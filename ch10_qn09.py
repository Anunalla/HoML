# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 20:26:21 2017

@author: kanmani
"""

import tensorflow as tf
import numpy as np
tf.reset_default_graph()
n_inputs =28*28
n_hidden1=300
n_hidden2=100
n_outputs = 10
learning_rate=0.01

X=tf.placeholder(tf.float32,shape=(None,n_inputs),name='X')
y=tf.placeholder(tf.int64,shape=(None),name='y')

with tf.name_scope("dnn"):
    hidden1=tf.contrib.layers.fully_connected(X,n_hidden1,scope="hidden1")
    hidden2=tf.contrib.layers.fully_connected(hidden1,n_hidden2,scope="hidden2")
    logits=tf.contrib.layers.fully_connected(hidden2,n_outputs,scope="outputs",activation_fn=None)
with tf.name_scope("loss"):
    xentropy =tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y,logits=logits)
    loss =tf.reduce_mean(xentropy,name="loss")
    loss_summary=tf.summary.scalar("log_loss",loss)
with tf.name_scope("train"):
    optimizer=tf.train.GradientDescentOptimizer(learning_rate)
    training_op=optimizer.minimize(loss)
with tf.name_scope("eval"):
    correct=tf.nn.in_top_k(logits,y,1)
    accuracy=tf.reduce_mean(tf.cast(correct,tf.float32))
    
init =tf.global_variables_initializer()
saver =tf.train.Saver()

from tensorflow.examples.tutorials.mnist import input_data
mnist=input_data.read_data_sets("/tmp/data/")

n_epochs=400
batch_size=50

with tf.Session() as sess:
    sess.run(init)
    for epoch in range(n_epochs):
        for iteration in range(mnist.train.num_examples//batch_size):
            X_batch,y_batch =mnist.train.next_batch(batch_size)
            sess.run(training_op,feed_dict={X:X_batch,y:y_batch})
        acc_train=accuracy.eval(feed_dict={X:X_batch,y:y_batch})
        acc_test=accuracy.eval(feed_dict={X:mnist.test.images,y:mnist.test.labels})
        
        print(epoch, "Train accuracy:", acc_train,"Test accuracy:",acc_test)
    save_path=saver.save(sess,"./my_model_final.ckpt")
    