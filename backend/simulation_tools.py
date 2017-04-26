import numpy as np

class Simulator(object):
    def __init__(self,  params, weights_path):
        N_in    = self.N_in       = params['N_in']
        N_rec   = self.N_rec      = params['N_rec']
        N_out   = self.N_out      = params['N_out']

        # Physical parameters
        self.dt = params['dt']
        self.tau = params['tau']
        self.alpha = params['alpha']
        self.dale_ratio = params['dale_ratio']
        self.rec_noise  = params['rec_noise']

        # Dale matrix
        dale_vec = np.ones(N_rec)
        if self.dale_ratio:
            dale_vec[int(self.dale_ratio * N_rec):] = -1
            self.dale_rec = np.diag(dale_vec)
            dale_vec[int(self.dale_ratio * N_rec):] = 0
            self.dale_out = np.diag(dale_vec)
        else:
            self.dale_rec = np.diag(dale_vec)
            self.dale_out = np.diag(dale_vec)

        # Connectivity
        self.connect_mat = np.ones((N_rec, N_rec))
        autapse = self.autapse = params.get('autapse', True)
        if not autapse:
            self.connect_mat -= np.diag(np.ones(N_rec))


        # Trained matrices
        weights = np.load(weights_path)
        self.W_in  = weights['W_in'] * weights['input_Connectivity']
        self.W_rec = weights['W_rec'] * weights['rec_Connectivity']
        self.W_out = weights['W_out'] * weights['output_Connectivity']

        self.b_rec = weights['b_rec']
        self.b_out = weights['b_out']

        # Initial state
        self.init_state = weights['init_state']

    def rnn_step(self, state, rnn_in):
        if self.dale_ratio:
            new_state = (1-self.alpha) * state \
                        + self.alpha * (np.matmul(np.maximum(state, np.zeros(state.shape)),
                                np.transpose(np.matmul(np.absolute(self.W_rec) * self.connect_mat, self.dale_rec)))
                            + np.matmul(rnn_in, np.transpose(np.absolute(self.W_in)) )
                            + self.b_rec)\
                        + np.sqrt(2.0 * self.alpha * self.rec_noise * self.rec_noise) * np.random.normal(loc=0.0, scale=1.0, size=state.shape)

            new_output = \
                        np.matmul(
                            np.maximum(new_state, np.zeros(state.shape)),
                            np.transpose(np.matmul(
                                np.absolute(self.W_out),
                                self.dale_out)))\
                        + self.b_out

            return new_output, new_state

    # apply the step to a full input vector
    def run_trial(self, trial_input):

        rnn_inputs = np.split(trial_input, trial_input.shape[0], axis=0)
        state = np.expand_dims(self.init_state[0, :], 0)
        rnn_outputs = []
        rnn_states = []
        for rnn_input in rnn_inputs:
            output, state = self.rnn_step(state, rnn_input)
            rnn_outputs.append(output)
            rnn_states.append(state)
        return np.array(rnn_outputs), np.array(rnn_states)


    #apply the RNN to a whole batch of inputs
    def run_trials(self, trial_input, batch_size):

        rnn_inputs = np.split(trial_input, trial_input.shape[1], axis=1)
        state = np.expand_dims(self.init_state[0, :], 0)
        state = np.repeat(state, batch_size, 0)
        rnn_outputs = []
        rnn_states = []
        for rnn_input in rnn_inputs:
            output, state = self.rnn_step(state, rnn_input)
            rnn_outputs.append(output)
            rnn_states.append(state)
        return np.array(rnn_outputs), np.array(rnn_states)
