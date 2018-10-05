# Project Sisyphus

This is an ongoing long-term project to develop a concise and easy-to-use package for the modeling and analysis of neural network dynamics. 

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

#### pip install
pip install **

#### alternative install
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