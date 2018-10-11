# Project Sisyphus

This is package is intended to help cognitive scientist translate task designs of interest into a form capable of being used as training data for a recurrent neural network.


We have isolated the front-end task design, in which users can intuitively describe the conditional logic of their task from the backend where gradient descent based optimization occurs. This is intended to facilitate researchers who might otherwise not have an easy implementation available to design and test hypothesis regarding the behavior of recurrent neural networks in different task environements.


Code is written and upkept by: @davidbrandfonbrener @dbehrlic @ABAtanasov @syncrostone 

## 17 Lines Introduction

A minimal introduction to our package. In this simple introduction you can generate a new recurrent neural network model, train that model on the random dot motion discrimination task, and plot out an example output in just 17 lines.

	import sisyphus2  
	from sisyphus2.tasks import rdm as rd  
	from sisyphus2.backend.models.basic import Basic  
	import tensorflow as tf  

	from matplotlib import pyplot as plt  
	%matplotlib inline

	rdm = rd.RDM(dt = 10, tau = 100, T = 2000, N_batch = 128)  
	gen = rdm.batch_generator()

	params = rdm.__dict__  
	params['name'] = 'model'  
	params['N_rec'] = 50  

	model = Basic(params)  
	model.build()  
	model.train(gen)

	x,_,_ = gen.next()

	plt.plot(model.test(x)[0][0,:,:])

	model.destruct()



## Writing a New Task

	Class your_new_class(Task):

		def __init__(self, N_in, N_out,dt, tau, T, N_batch):
	        super(RDM,self).__init__(N_in, N_out, dt, tau, T, N_batch)

		def generate_trial_params(self,batch,trial):

			''' function that produces trial specific params for your task (e.g. coherence for the random dot motion discrimination task)

			Args:
				batch: # of batch for training (for internal use)
				trial: # of trial within a batch (for internal use)

			Returns:
				params: A dictionary of necessary params for trial_function

				'''

		def trial_function(self,t,params):

			'''function that specifies network input, target output and loss mask for your task.

			Args:
				t: time
				params: params dictionary from generate_trial_params

			Returns:
				x_t: input vector at time t
				y_t: target output vector at time t
				mask_t: loss function mask at time t

				'''

## Building a New Model

- basic
- lstm

Extensibility:

	def
	- recurrent_timestep
	- output_timestep
	- forward_pass

### Backend

- initializations
- loss_functions
- regularizations
- rnn
- simulation


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

git clone -b networks-branch https://github.com/dbehrlich/sisyphus2.git  
python setup.py install

#### Alternative Install

pip install **


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