import tensorflow as tf
from attacks.base_attack import BaseAttack


class ScalingAttack(BaseAttack):
    def __init__(self, scale_factor=0.5, **kwargs):
        """
        Scaling attack that downsamples and upsamples back
        
        Args:
            scale_factor: Factor to scale down (0.5 = 50%, 0.75 = 75%)
        """
        super(ScalingAttack, self).__init__()
        self.scale_factor = scale_factor

    def scale(self, inputs):
        """
        Downsample the image then upsample back to original size
        """
        original_shape = tf.shape(inputs)
        height = original_shape[1]
        width = original_shape[2]
        
        # Random scale factor between 50% and 75%
        scale_factor = tf.random.uniform([], minval=0.5, maxval=0.75)
        
        # Calculate new dimensions
        new_height = tf.cast(tf.cast(height, tf.float32) * scale_factor, tf.int32)
        new_width = tf.cast(tf.cast(width, tf.float32) * scale_factor, tf.int32)
        
        # Downsample using bilinear interpolation
        downsampled = tf.image.resize(inputs, 
                                      [new_height, new_width], 
                                      method='bilinear')
        
        # Upsample back to original size
        upsampled = tf.image.resize(downsampled, 
                                    [height, width], 
                                    method='bilinear')
        
        return upsampled

    def call(self, inputs):
        outputs = self.scale(inputs)
        return outputs


def scaling_function(x):
    return ScalingAttack()(x)
