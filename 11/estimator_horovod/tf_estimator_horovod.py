"""#"""
import os
import sys
import time
import json
import tensorflow as tf
import horovod.tensorflow as hvd

import args_parser
from datasets import cifar10
from nets import nets_factory
from utils import hooks
from datetime import datetime

TIMES = '/home/sam14/sam14015/task/11/estimator_horovod/out.csv'

class Model(object):
	"""Class that defines a graph for image classification."""
	def __init__(self, params, training):
		self.network_fn = nets_factory.get_network_fn(
			params.model_name,
			num_classes=params.num_classes,
			is_training=training)

	def __call__(self, inputs):
		logits, end_points = self.network_fn(inputs)
		return logits, end_points


def model_fn(features, labels, mode, params):
	"""The model_fn argument for creating an Estimator."""
	
	global_step = tf.train.get_global_step()
	model = Model(params, training=(mode == tf.estimator.ModeKeys.TRAIN))
	images = features
	tf.summary.image('images', images, max_outputs=3)

	logits, end_points = model(images)
	predictions = tf.argmax(logits, axis=1)
	#probabilities = tf.nn.softmax(logits)


	with tf.name_scope('loss'):		   
		cross_entropy = tf.losses.sparse_softmax_cross_entropy(
			labels=labels, logits=logits, scope='xent_loss')
		tf.summary.scalar('xent_loss', cross_entropy)

	with tf.name_scope('accuracy'):
		accuracy = tf.metrics.accuracy(
			labels=labels, predictions=predictions, name='acc')
		tf.summary.scalar('accuracy', accuracy[1])

	if mode == tf.estimator.ModeKeys.EVAL:
		return tf.estimator.EstimatorSpec(
			mode=mode,
			loss=cross_entropy,
			eval_metric_ops={'accuracy/accuracy': accuracy})

	with tf.name_scope('train_op'):
		# Horovod: add Horovod Distributed Optimizer.
		# Note: Allgather allocates an output tensor which is proportionate to
		# the number of processes participating in the training. If you find
		# yourself running out of GPU memory, you can force allreduce to happen
		# on CPU by passing `device_sparse='/cpu:0'`.
		# optimizer = hvd.DistributedOptimizer(optimizer, device_dense='/cpu:0')

		optimizer = tf.train.GradientDescentOptimizer(learning_rate=params.learning_rate)
		optimizer = hvd.DistributedOptimizer(optimizer)
		train_op = optimizer.minimize(cross_entropy,global_step=global_step)

	train_hook_list = []
	train_tensors_log = {'accuracy': accuracy[1],
						 'loss': cross_entropy,
						 'global_step': global_step}
	train_hook_list.append(tf.train.LoggingTensorHook(
		tensors=train_tensors_log, every_n_iter=params.log_every_n_steps))

	# Horovod: BroadcastGlobalVariablesHook broadcasts initial variable states from
	# rank 0 to all other processes. This is necessary to ensure consistent
	# initialization of all workers when training is started with random weights or
	# restored from a checkpoint.
	train_hook_list.append(hvd.BroadcastGlobalVariablesHook(0))


	# Hook to print examples per second. Hook defines in utils->hooks
	train_hook_list.append(hooks.ExamplesPerSecondHook(
			batch_size=params.batch_size, warm_steps=10, metric_logger=None,
			every_n_steps=params.log_every_n_steps))

	if mode == tf.estimator.ModeKeys.TRAIN:		   
		return tf.estimator.EstimatorSpec(
			mode=mode,
			loss=cross_entropy,
			train_op=train_op,
			training_hooks=train_hook_list)


def main(_):

	hvd.init()

	# Load params passed by Flags
	hparams = tf.contrib.training.HParams()
	for key, val in vars(FLAGS).items():
		hparams.add_hparam(key, val)

  
	# Horovod: pin GPU to be used to process local rank (one GPU per process)
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	config.gpu_options.visible_device_list = str(hvd.local_rank())

	# Load and set train_image_size to resize image
	network_fn = nets_factory.get_network_fn(
		hparams.model_name, num_classes=hparams.num_classes)
	hparams.set_hparam(
		'train_image_size',
		hparams.train_image_size or network_fn.default_image_size)
	del network_fn

	hparams.set_hparam(
		'preprocessing_name',
		hparams.preprocessing_name or hparams.model_name)


	# Horovod: save checkpoints only on worker 0 to prevent other workers from
	# corrupting them.
	model_dir = hparams.model_dir if hvd.rank() == 0 else None		  

	image_classifier = tf.estimator.Estimator(
		model_fn=model_fn,
		model_dir=model_dir,
		config=tf.estimator.RunConfig(session_config=config,
			save_checkpoints_secs=None,
			save_checkpoints_steps=None),
		params=hparams)

	# Train and eval input functions
	# train_input_fn = (lambda: cifar10.get_ds(
	#	  hparams, 'train', mode=tf.estimator.ModeKeys.TRAIN, file_pattern=_FILE_PATTERN))
	train_input_fn = (lambda: cifar10.get_ds(
		hparams, 'train', mode=tf.estimator.ModeKeys.TRAIN))
	eval_input_fn = (lambda: cifar10.get_ds(
		hparams, 'test', mode=tf.estimator.ModeKeys.EVAL))

	if hvd.rank() == 0:
		#measure t1
		t1 = time.time()
		print(" Date is now: {}".format(str(datetime.now())), file=sys.stderr)

	max_steps = hparams.max_number_of_steps

	print(" ---------------------- Starting train for {} ----------------------".format(hvd.rank()), file=sys.stderr)

	# Divide max_number_steps by number of gpus
	image_classifier.train(input_fn=train_input_fn,
							   #max_steps=hparams.max_number_of_steps)
							   max_steps=hparams.max_number_of_steps // hvd.size())
	#barrier
	print(" ---------------------- Stopping train for {} ----------------------".format(hvd.rank()), file=sys.stderr)

	if hvd.rank() == 0:
		#measure t2
		t2 = time.time()
		t = t2 - t1
		print(" ---------------------- Training took {} s ----------------------".format(t), file=sys.stderr)

		with open(TIMES, 'a') as f:
			f.write("{}\t{}\t{}\t{:.2f}\n".format(
				hparams.model_name,
				max_steps,
				hvd.size(),
				t))

		# Skip the evaluation
		#image_classifier.evaluate(input_fn=eval_input_fn)




if __name__ == '__main__':
	tf.logging.set_verbosity(tf.logging.INFO)
	parser = args_parser.FuncArgParser()
	FLAGS, unparsed = parser.parse_known_args()
	tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
