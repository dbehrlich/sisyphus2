# Project Sisyphus

This is package is intended to help cognitive scientist translate task designs of interest into a form capable of being used as training data for a recurrent neural network.


We have isolated the front-end task design, in which users can intuitively describe the conditional logic of their task from the backend where gradient descent based optimization occurs. This is intended to facilitate researchers who might otherwise not have an easy implementation available to design and test hypothesis regarding the behavior of recurrent neural networks in different task environements.

## Package Structure

### Tasks

task superclass

Extensibility 

- generate_trial_params
- trial_function

### Models

- basic
- lstm

### Backend

- initializations
- loss_functions
- regularizations
- rnn
- simulation

Code is written and upkept by: @davidbrandfonbrener @dbehrlic @ABAtanasov @syncrostone 


## Install

### Dependencies

- Numpy
- Tensorflow
- Python=2.7

For Demos:
- Jupyter
- Ipython
- Matplotlib

### Installation

pip install **

#### Alternative Install
git clone -b networks-branch https://github.com/dbehrlich/sisyphus2.git  
python setup.py install


## Params

### Task:
- N_batch
- N_in
- N_out
- T
- dt
- tau
- stim_noise

  
(plus other params specific to the task)

implicit params:
  - alpha
  - N_steps


### Model:
- name
- N_rec
- N_in
- N_out
- N_steps
- dt
- tau
- dale_ratio
- rec_noise
- load_weights_path
- initializer 
-  trainability (many boolean variables)

implicit params:
  - alpha
  - N_batch


### Train:
- learning_rate
- training_iters
- loss_epoch
- verbosity
- save_weights_path
- save_training_weights_epoch
- training_weigts_path
- generator_function
- optimizer
- clip_grads