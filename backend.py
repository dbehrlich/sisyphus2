from __future__ import print_function

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt



class Model(object):

    def __init__(self, n_in, n_hidden, n_out, n_steps, tau, dale_ratio, rec_noise, batch_size):
        #network size
        self.n_in = n_in
        self.n_hidden = n_hidden
        self.n_out = n_out
        self.n_steps = n_steps
        self.batch_size = batch_size

        #neuro parameters
        self.tau = tau
        self.alpha = 1.0 - tau
        self.dale_ratio = dale_ratio
        self.rec_noise = rec_noise

        #dale matrix
        dale_vec = np.ones(n_hidden)
        dale_vec[int(dale_ratio * n_hidden):] = -1
        self.dale = np.diag(dale_vec)

        #tensorflow initializations
        self.x = tf.placeholder("float", [batch_size, n_steps, n_in])
        self.y = tf.placeholder("float", [batch_size, n_steps, n_out])
        self.init_state = tf.random_normal([batch_size, n_hidden], mean=0.0, stddev=rec_noise)

        # trainable variables
        with tf.variable_scope('model'):
            # U = tf.get_variable('U', [n_in, n_hidden])
            # W = tf.get_variable('W', [n_hidden, n_hidden])
            # Z = tf.get_variable('Z', [n_hidden, n_out])
            # Dale = tf.get_variable('Dale', [n_hidden, n_hidden], initializer=tf.constant_initializer(self.dale),
            #                        trainable=False)
            # brec = tf.get_variable('brec', [n_hidden], initializer=tf.constant_initializer(0.0))
            # bout = tf.get_variable('bout', [n_hidden], initializer=tf.constant_initializer(0.0))

            self.predictions, self.states = self.compute_predictions()
            self.loss = self.reg_loss()

    #implement one step of the RNN
    def rnn_step(self, rnn_in, state):
        with tf.variable_scope('rnn_step'):
            U = tf.get_variable('U', [self.n_in, self.n_hidden])
            W = tf.get_variable('W', [self.n_hidden, self.n_hidden])
            Z = tf.get_variable('Z', [self.n_hidden, self.n_out])
            Dale = tf.get_variable('Dale', [self.n_hidden, self.n_hidden], initializer=tf.constant_initializer(self.dale),
                                   trainable=False)
            brec = tf.get_variable('brec', [self.n_hidden], initializer=tf.constant_initializer(0.0))
            bout = tf.get_variable('bout', [self.n_hidden], initializer=tf.constant_initializer(0.0))

            new_state = state * self.tau + self.alpha * (tf.matmul(tf.nn.relu(state), tf.matmul(tf.abs(W), Dale))
                + tf.matmul(tf.abs(rnn_in), U) + brec) + tf.random_normal(state.get_shape(), mean=0.0, stddev=self.rec_noise)
            # Is this next line right????
            new_output = tf.matmul(tf.nn.relu(new_state), tf.matmul(Dale, tf.abs(Z))) + bout
        return new_output, new_state

    #apply the step to a full input vector
    def compute_predictions(self):
        rnn_inputs = tf.unpack(self.x, axis=1)

        state = self.init_state
        rnn_outputs = []
        rnn_states = []
        for rnn_input in rnn_inputs:
            output, state = self.rnn_step(rnn_input, state)
            rnn_outputs.append(output)
            rnn_states.append(state)

        return tf.transpose(rnn_outputs, [1, 0, 2]), tf.transpose(rnn_states, [1, 0, 2])
        #return tf.scan(self.rnn_step, tf.transpose(self.x, [1,0,2]), initializer = self.init_state)

    #regularized loss function
    def reg_loss(self):
        return tf.reduce_mean(tf.square(self.predictions - self.y))

#train the model using Adam
def train(sess, model, generator, learning_rate, training_iters, batch_size, display_step):

    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(model.loss)
    sess.run(tf.initialize_all_variables())
    step = 1
    # Keep training until reach max iterations
    while step * batch_size < training_iters:
        batch_x, batch_y, mask = generator()
        sess.run(optimizer, feed_dict={x: batch_x, y: batch_y})
        if step % display_step == 0:
            # Calculate batch loss
            loss = sess.run(cost, feed_dict={x: batch_x, y: batch_y})
            print("Iter " + str(step * batch_size) + ", Minibatch Loss= " + \
                  "{:.6f}".format(loss))
        step += 1
    print("Optimization Finished!")

#use a trained model to get test outputs
def test(self):
    return


# # Parameters
# learning_rate = 0.001
# training_iters = 200000
# n_steps = 800 # timesteps per sequence of the input
# batch_size = 128
# display_step = 10
#
# tau = 1.0
# alpha = 1.0 - tau
# dale_ratio = 0.8
# rec_noise = .1
#
#
# # Network Parameters
# n_in = 2 #ins
# n_hidden = 10 # hidden layer num of features
# n_out = 1 # outs
#
#
# # tf Graph input
# x = tf.placeholder("float", [batch_size, n_steps, n_in])
# y = tf.placeholder("float", [batch_size, n_steps, n_out])
# init_state = tf.random_normal([batch_size, n_hidden], mean=0.0, stddev=rec_noise)
#
# #dale's ratio matrix
# dale_vec = np.ones(n_hidden)
# dale_vec[int(dale_ratio*n_hidden):] = -1
# dale = np.diag(dale_vec)
#
# #trainable variables
# with tf.variable_scope('rnn_cell'):
#     U = tf.get_variable('U', [n_in, n_hidden])
#     W = tf.get_variable('W', [n_hidden, n_hidden])
#     Z = tf.get_variable('Z', [n_hidden, n_out])
#     Dale = tf.get_variable('Dale', [n_hidden, n_hidden], initializer=tf.constant_initializer(dale), trainable=False)
#     brec = tf.get_variable('brec', [n_hidden], initializer=tf.constant_initializer(0.0))
#     bout = tf.get_variable('bout', [n_hidden], initializer=tf.constant_initializer(0.0))
#
#
# #step function
# #returns new_output, new_state
# def rnn_cell(rnn_in, state):
#     with tf.variable_scope('rnn_cell', reuse=True):
#         U = tf.get_variable('U')
#         W = tf.get_variable('W')
#         Z = tf.get_variable('Z')
#         brec = tf.get_variable('brec')
#         bout = tf.get_variable('bout')
#         Dale = tf.get_variable('Dale')
#         new_state = state * tau + alpha * (tf.matmul(tf.nn.relu(state), tf.matmul(tf.abs(W), Dale)) + tf.matmul(tf.abs(rnn_in), U) + brec) \
#             + tf.random_normal(state.get_shape(), mean=0.0, stddev=rec_noise)
#         #Is this next line right????
#         new_output = tf.matmul(tf.nn.relu(new_state), tf.matmul(Dale, tf.abs(Z))) + bout
#     return new_output, new_state
#
#
# def RNN(x):
#     rnn_inputs = tf.unpack(x, axis=1)
#
#     state = init_state
#     rnn_outputs = []
#     rnn_states = []
#     for rnn_input in rnn_inputs:
#         output, state = rnn_cell(rnn_input, state)
#         rnn_outputs.append(output)
#         rnn_states.append(state)
#
#     return tf.transpose(rnn_outputs, [1, 0, 2])
#
#
# def reg_loss(pred, y):
#     return tf.reduce_mean(tf.square(pred - y))
#
#
#
# pred = RNN(x)
#
# # Define loss and optimizer
# cost = reg_loss(pred, y)
# optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
#
# # Initializing the variables
# init = tf.initialize_all_variables()
#
#
# # Launch the graph
# with tf.Session() as sess:
#     sess.run(init)
#     step = 1
#     params = set_params(sample_size= 128, input_wait=50, stim_dur=50, quiet_gap=100, nturns=5)
#     # Keep training until reach max iterations
#     while step * batch_size < training_iters:
#         batch_x, batch_y, mask = generate_trials(params)
#         sess.run(optimizer, feed_dict={x: batch_x, y: batch_y})
#         if step % display_step == 0:
#             # Calculate batch loss
#             loss = sess.run(cost, feed_dict={x: batch_x, y: batch_y})
#             print("Iter " + str(step*batch_size) + ", Minibatch Loss= " + \
#                   "{:.6f}".format(loss) )
#         step += 1
#     print("Optimization Finished!")
#     wrec = sess.run(W)

