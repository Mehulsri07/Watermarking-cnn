import tensorflow as tf
from attacks.base_attack import BaseAttack


class CroppingAttack(BaseAttack):
    def __init__(self, crop_percentage=0.1, **kwargs):
        """
        Crop attack that removes edges and pads back to original size
        
        Args:
            crop_percentage: Percentage to crop from each edge (0.05 to 0.15)
        """
        super(CroppingAttack, self).__init__()
        self.crop_percentage = crop_percentage

    def crop(self, inputs):
        """
        Crop the image by removing edges, then pad back to original size
        """
        batch_size = tf.shape(inputs)[0]
        height = tf.shape(inputs)[1]
        width = tf.shape(inputs)[2]
        channels = tf.shape(inputs)[3]
        
        # Calculate crop amount (random between 5% and 15%)
        crop_ratio = tf.random.uniform([], minval=0.05, maxval=0.15)
        
        # Calculate crop dimensions
        crop_h = tf.cast(tf.cast(height, tf.float32) * crop_ratio, tf.int32)
        crop_w = tf.cast(tf.cast(width, tf.float32) * crop_ratio, tf.int32)
        
        # Crop from all sides
        cropped = inputs[:, crop_h:height-crop_h, crop_w:width-crop_w, :]
        
        # Pad back to original size with zeros (black padding)
        pad_h = crop_h
        pad_w = crop_w
        
        padded = tf.pad(cropped, 
                       [[0, 0], [pad_h, pad_h], [pad_w, pad_w], [0, 0]], 
                       mode='CONSTANT', 
                       constant_values=0)
        
        # Ensure output shape matches input shape
        padded = tf.image.resize_with_crop_or_pad(padded, height, width)
        
        return padded

    def call(self, inputs):
        outputs = self.crop(inputs)
        return outputs


def cropping_function(x):
    return CroppingAttack()(x)
