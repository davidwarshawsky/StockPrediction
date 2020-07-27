import tensorflow as tf
import os
from functools import wraps

# https://www.tensorflow.org/guide/tpu

resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu='grpc://' + os.environ['COLAB_TPU_ADDR'])
tf.config.experimental_connect_to_cluster(resolver)
# This is the TPU initialization code that has to be at the beginning.
tf.tpu.experimental.initialize_tpu_system(resolver)
print("All devices: ", tf.config.list_logical_devices('TPU'))


def run_on_device(device=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            if device == 'TPU' and check_tpu_availability():
                resolver = tf.distribute.cluster_resolver.TPUClusterResolver(
                    tpu='grpc://' + os.environ['COLAB_TPU_ADDR'])
                tf.config.experimental_connect_to_cluster(resolver)
                # This is the TPU initialization code that has to be at the beginning.
                tf.tpu.experimental.initialize_tpu_system(resolver)
                print("All devices: ", tf.config.list_logical_devices('TPU'))
                strategy = tf.distribute.experimental.TPUStrategy(resolver)
                with strategy.scope():
                    return func(*args,**kwargs)
            elif device == 'GPU':
                config = tf.compat.v1.ConfigProto()
                config.gpu_options.allow_growth = True
                with tf.device('/gpu:0'):
                    return func(*args,**kwargs)
            else:
                return func(*args,**kwargs)
        return wrapper
    return decorator



def check_tpu_availability():
    try:
        device_name = os.environ['COLAB_TPU_ADDR']
        TPU_ADDRESS = 'grpc://' + device_name
        print('Found TPU at: {}'.format(TPU_ADDRESS))
        return True

    except KeyError:
        print('TPU not found')
        return False

def manual_device_placement_example():
    a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])

    with tf.device('/TPU:0'):
        c = tf.matmul(a, b)
    print("c device: ", c.device)
    print(c)



def keras_model_to_tpu(model):
    tpu_model = tf.contrib.tpu.keras_to_tpu_model(
        model,
        strategy=tf.contrib.tpu.TPUDistributionStrategy(
            tf.contrib.cluster_resolver.TPUClusterResolver(
                tpu='grpc://' + os.environ['COLAB_TPU_ADDR'])
        )
    )
    return tpu_model


def keras_estimator_to_tpu(model):
    """
    Estimators should be added at TensorFlow’s model level.
    Standard estimators can run models on CPUs and GPUs.
     But you need to use tf.contrib.tpu.TPUEstimator to train a model using the TPU.
    :param model:
    :return:
    """
    my_tpu_estimator = tf.contrib.tpu.TPUEstimator(
        model_fn=model,
        config=tf.contrib.tpu.RunConfig(),
        use_tpu=False)
    # I think the "use_tpu" should be True but it says False in the article
    return my_tpu_estimator


def tpu_config_operation(master,FLAGS):
    my_tpu_run_config = tf.contrib.tpu.RunConfig(
        master=master,
        evaluation_master=master,
        model_dir=FLAGS.model_dir,
        session_config=tf.ConfigProto(
            allow_soft_placement=True, log_device_placement=True),
        tpu_config=tf.contrib.tpu.TPUConfig(FLAGS.iterations,
                                            FLAGS.num_shards),
    )



# https://heartbeat.fritz.ai/step-by-step-use-of-google-colab-free-tpu-75f8629492b3

if __name__ == '__main__':
    manual_device_placement_example()

