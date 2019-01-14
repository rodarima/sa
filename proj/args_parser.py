"""#"""
import argparse


class FuncArgParser(argparse.ArgumentParser):
    """Arguments for configuring and running a Model."""

    def __init__(self):
        super(FuncArgParser, self).__init__()

        self.add_argument(
            '--model_dir',
            type=str,
            help='Directory where checkpoints and event logs are written to.')

        self.add_argument(
            '--num_classes',
            type=int,
            help='Number of classes in the dataset.')

        self.add_argument(
            '--num_epochs',
            type=int,
            default=None,
            help='Number of iterations of the whole dataset.')

        self.add_argument(
            '--num_preprocessing_threads',
            type=int,
            default=4,
            help='The number of threads used to process the input items.')

        self.add_argument(
            '--log_every_n_steps',
            type=int,
            default=10,
            help='The frequency with which logs are print.')

        self.add_argument(
            '--save_summary_steps',
            type=int,
            default=100,
            help='The frequency with which summaries are saved, in steps.')

        self.add_argument(
            '--save_checkpoints_steps',
            type=int,
            default=200,
            help='The frequency with which the model is saved, in steps.')

        # Optimization Flags

        self.add_argument(
            '--weight_decay',
            type=float,
            default=0.00004,
            help='The weight decay on the model weights.')


        # Learning Rate Flags

        self.add_argument(
            '--learning_rate_decay_type',
            type=str,
            default='exponential',
            choices=['fixed', 'exponential', 'polynomial'],
            help='Specifies how the learning rate is decayed. One of "fixed", '
            '"exponential", or "polynomial".')

        self.add_argument(
            '--learning_rate',
            type=float,
            default=0.01,
            help='Initial learning rate.')

        self.add_argument(
            '--end_learning_rate',
            type=float,
            default=0.0001,
            help='The minimal end learning rate used by a polynomial decay '
            'learning rate.')

        self.add_argument(
            '--label_smoothing',
            type=float,
            default=0.0,
            help='The amount of label smoothing.')

        self.add_argument(
            '--learning_rate_decay_factor',
            type=float,
            default=0.94,
            help='Learning rate decay factor.')

        self.add_argument(
            '--num_epochs_per_decay',
            type=float,
            default=2.0,
            help='Number of epochs after which learning rate decays.')

        # Dataset Flags

        self.add_argument(
            '--dataset_name',
            type=str,
            default='imagenet',
            help='The name of the dataset to load.')

        self.add_argument(
            '--dataset_split_name',
            type=str,
            default='train',
            help='The name of the train/test split.')

        self.add_argument(
            '--dataset_file_pattern',
            type=str,
            help='The file pattern to use for matching '
            'the dataset source files.')

        self.add_argument(
            '--train_dir',
            type=str,
            help='Path or directory containing the train dataset.')

        self.add_argument(
            '--eval_dir',
            type=str,
            help='Path or directory containing the eval dataset.')

        self.add_argument(
            '--labels_offset',
            type=int,
            default=0,
            help='An offset for the labels in the dataset. This flag is '
            'primarily used to evaluate the VGG and ResNet architectures which '
            'do not use a background class for the ImageNet dataset.')

        self.add_argument(
            '--model_name',
            type=str,
            help='The name of the architecture to train.')

        self.add_argument(
            '--preprocessing_name',
            type=str,
            default=None,
            help='The name of the preprocessing to use. If left as `None`, '
            'then the model_name flag is used.')

        self.add_argument(
            '--batch_size',
            type=int,
            help='The number of samples in each batch.')

        self.add_argument(
            '--train_image_size',
            type=int,
            default=None,
            help='Train image size.')

        self.add_argument(
            '--max_number_of_steps',
            type=int,
            default=None,
            help='The maximum number of training steps.')


        # Fine-Tuning Flags

        self.add_argument(
            '--checkpoint_dir',
            type=str,
            default=None,
            help='The dir or path to a checkpoint from which to fine-tune.')

        self.add_argument(
            '--checkpoint_exclude_scopes',
            type=str,
            default=None,
            help='Comma-separated list of scopes of variables to exclude when '
            'restoring from a checkpoint.')

        self.add_argument(
            '--trainable_scopes',
            type=str,
            default=None,
            help='Comma-separated list of scopes to filter the set of '
            'variables to train. `None` would train all the variables.')


        # Training parameters

        self.add_argument(
            '--data_format',
            type=str,
            default=None,
            choices=['channels_first', 'channels_last'],
            help='A flag to override the data format used in the model. '
            'channels_first provides a performance boost on GPU but is not '
            'always compatible with CPU. If left unspecified, the data format '
            'will be chosen automatically based on whether TensorFlow was '
            'built for CPU or GPU.')

        self.add_argument(
            '--export_dir',
            type=str,
            help='The directory where the exported SavedModel will be stored.')

        self.add_argument(
            '--num_ckpt',
            type=int,
            default=3,
            help='Number of checkpoints to store.')

        self.add_argument(
            '--eval_throttle_secs',
            type=int,
            default=1200,
            help='Number of checkpoints to store.')

