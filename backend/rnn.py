from __future__ import print_function

import tensorflow as tf
import numpy as np
from time import time
from regularizations import Regularizer
from loss_functions import LossFunction
from initializations import WeightInitializer, GaussianSpectralRadius

class RNN(object):
    def __init__(self, params):
        self.params = params
        # ----------------------------------
        # Network sizes (tensor dimensions)
        # ----------------------------------
        N_in = self.N_in = params['N_in']
        N_rec = self.N_rec = params['N_rec']
        N_out = self.N_out = params['N_out']
        N_steps = self.N_steps = params['N_steps']
        N_batch = self.N_batch = params['N_batch']

        # ----------------------------------
        # Physical parameters
        # ----------------------------------
        self.dt = params['dt']
        self.tau = params['tau']
        self.alpha = self.dt / self.tau
        self.dale_ratio = params['dale_ratio']
        self.rec_noise = params['rec_noise']

        # ----------------------------------
        # Load weights path
        # ----------------------------------
        self.load_weights_path = params.get('load_weights_path', None)

        # ----------------------------------
        # Dale's law matrix
        # ----------------------------------
        dale_vec = np.ones(N_rec)
        if self.dale_ratio is not None:
            dale_vec[int(self.dale_ratio * N_rec):] = -1
            self.dale_rec = np.diag(dale_vec)
            dale_vec[int(self.dale_ratio * N_rec):] = 0
            self.dale_out = np.diag(dale_vec)
        else:
            self.dale_rec = np.diag(dale_vec)
            self.dale_out = np.diag(dale_vec)

        # ----------------------------------
        # Trainable features
        # ----------------------------------
        self.W_in_train = params.get('W_in_train', True)
        self.W_rec_train = params.get('W_rec_train', True)
        self.W_out_train = params.get('W_out_train', True)
        self.b_rec_train = params.get('b_rec_train', True)
        self.b_out_train = params.get('b_out_train', True)
        self.init_state_train = params.get('init_state_train', True)

        # ---------------------------------------
        # Tensorflow input/output initializations
        # ----------------------------------------
        self.x = tf.placeholder("float", [N_batch, N_steps, N_in])
        self.y = tf.placeholder("float", [N_batch, N_steps, N_out])
        self.output_mask = tf.placeholder("float", [N_batch, N_steps, N_out])

        # ------------------------------------------------
        # Define initializer for TensorFlow variables
        # ------------------------------------------------
        if self.load_weights_path is not None:
            self.initializer = WeightInitializer(load_weights_path=self.load_weights_path)
        else:
            self.initializer = params.get('initializer',
                                          GaussianSpectralRadius(N_in=N_in,
                                                                 N_rec=N_rec, N_out=N_out,
                                                                 autapses=True, spec_rad=1.1))


        # ------------------------------------------------
        # Trainable variables:
        # Initial State, weight matrices and biases
        # ------------------------------------------------

        self.init_state = tf.get_variable('init_state', [N_batch, N_rec],
                                          initializer=self.initializer.get('init_state'),
                                          trainable=self.init_state_train)

        # Input weight matrix:
        self.W_in = \
            tf.get_variable('W_in', [N_rec, N_in],
                            initializer=self.initializer.get('W_in'),
                            trainable=self.W_in_train)

        # Recurrent weight matrix:
        self.W_rec = \
            tf.get_variable(
                'W_rec',
                [N_rec, N_rec],
                initializer=self.initializer.get('W_rec'),
                trainable=self.W_rec_train)

        # Output weight matrix:
        self.W_out = tf.get_variable('W_out', [N_out, N_rec],
                                     initializer=self.initializer.get('W_out'),
                                     trainable=self.W_out_train)

        # Recurrent bias:
        self.b_rec = tf.get_variable('b_rec', [N_rec], initializer=self.initializer.get('b_rec'),
                                     trainable=self.b_rec_train)
        # Output bias:
        self.b_out = tf.get_variable('b_out', [N_out], initializer=self.initializer.get('b_out'),
                                     trainable=self.b_out_train)

        # ------------------------------------------------
        # Non-trainable variables:
        # Overall connectivity and Dale's law matrices
        # ------------------------------------------------

        # Recurrent Dale's law weight matrix:
        self.Dale_rec = tf.get_variable('Dale_rec', [N_rec, N_rec],
                                        initializer=tf.constant_initializer(self.dale_rec),
                                        trainable=False)

        # Output Dale's law weight matrix:
        self.Dale_out = tf.get_variable('Dale_out', [N_rec, N_rec],
                                        initializer=tf.constant_initializer(self.dale_out),
                                        trainable=False)

        # Connectivity weight matrices:
        self.input_connectivity = tf.get_variable('input_connectivity', [N_rec, N_in],
                                                  initializer=self.initializer.get('input_connectivity'),
                                                  trainable=False)
        self.rec_connectivity = tf.get_variable('rec_connectivity', [N_rec, N_rec],
                                                initializer=self.initializer.get('rec_connectivity'),
                                                trainable=False)
        self.output_connectivity = tf.get_variable('output_connectivity', [N_out, N_rec],
                                                   initializer=self.initializer.get('output_connectivity'),
                                                   trainable=False)



    def build(self):
        # --------------------------------------------------
        # Define the predictions
        # --------------------------------------------------
        self.predictions, self.states = self.forward_pass()

        # --------------------------------------------------
        # Define the loss (based on the predictions)
        # --------------------------------------------------
        self.loss = LossFunction(self.params).set_model_loss(self)

        # --------------------------------------------------
        # Define the regularization
        # --------------------------------------------------
        self.reg = Regularizer(self.params).set_model_regularization(self)

        # --------------------------------------------------
        # Define the total regularized loss
        # --------------------------------------------------
        self.reg_loss = self.loss + self.reg






    def recurrent_timestep(self, rnn_in, state):

        pass


    def output_timestep(self, state):

        pass


    def forward_pass(self):

        pass





    def save(self, sess, save_path):

        weights_dict = dict()

        for var in tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES):
            # avoid saving duplicates
            if var.name.endswith(':0'):
                name = var.name[:-2]
                weights_dict.update( {name: var.eval(session = sess)} )

        np.savez(save_path, **weights_dict)

        return


    def train(self, trial_batch_generator, train_params):

        t0 = time()
        # --------------------------------------------------
        # Extract params
        # --------------------------------------------------
        batch_size = train_params.get('batch_size', 64)
        learning_rate = train_params.get('learning_rate', .001)
        training_iters = train_params.get('training_iters', 50000)
        print_epoch = train_params.get('print_epoch', 10)
        save_weights_path = train_params.get('save_weights_path', None)
        save_training_weights_epoch = train_params.get('save_training_weights_epoch', 100)
        training_weights_path = train_params.get('training_weights_path', None)
        generator_function = train_params.get('generator function', None)
        optimizer = train_params.get('optimizer',
                                     tf.train.AdamOptimizer(learning_rate = learning_rate))
        clip_grads = train_params.get('clip_grads', True)

        # --------------------------------------------------
        # open a session
        # --------------------------------------------------
        sess = tf.Session()

        # --------------------------------------------------
        # Compute gradients
        # --------------------------------------------------
        grads = optimizer.compute_gradients(self.reg_loss)

        # --------------------------------------------------
        # Clip gradients
        # --------------------------------------------------
        if clip_grads:
            grads = [(tf.clip_by_norm(grad, 1.0), var)
                                if grad is not None else (grad, var)
                                for grad, var in grads]

        # --------------------------------------------------
        # Call the optimizer and initialize session
        # --------------------------------------------------
        optimize = optimizer.apply_gradients(grads)
        sess.run(tf.global_variables_initializer())
        epoch = 1

        # --------------------------------------------------
        # Record training time for performance benchmarks
        # --------------------------------------------------
        t1 = time()

        # --------------------------------------------------
        # Training loop
        # --------------------------------------------------
        while epoch * batch_size < training_iters:
            batch_x, batch_y, output_mask = trial_batch_generator.next()
            sess.run(optimize, feed_dict={self.x: batch_x, self.y: batch_y, self.output_mask: output_mask})
            # --------------------------------------------------
            # Output batch loss
            # --------------------------------------------------
            if epoch % print_epoch == 0:
                reg_loss = sess.run(self.reg_loss,
                                feed_dict={self.x: batch_x, self.y: batch_y, self.output_mask: output_mask})
                print("Iter " + str(epoch * batch_size) + ", Minibatch Loss= " + \
                      "{:.6f}".format(reg_loss))

                # --------------------------------------------------
                # Allow for curriculum learning
                # --------------------------------------------------
                if generator_function is not None:
                    trial_batch_generator = generator_function(reg_loss, epoch)

            # --------------------------------------------------
            # Save intermediary weights
            # --------------------------------------------------
            if epoch % save_training_weights_epoch == 0:
                if training_weights_path is not None:
                    self.save(sess, training_weights_path + str(epoch))

            epoch += 1

        t2 = time()
        print("Optimization finished!")

        # --------------------------------------------------
        # Save final weights
        # --------------------------------------------------
        if save_weights_path is not None:
            self.save(sess, save_weights_path)
            print("Model saved in file: %s" % save_weights_path)

        # --------------------------------------------------
        # Close session
        # --------------------------------------------------
        sess.close()

        return (t2 - t1), (t1 - t0)




