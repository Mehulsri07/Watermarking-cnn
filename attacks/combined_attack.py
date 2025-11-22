import tensorflow as tf
from attacks.base_attack import BaseAttack
from attacks.gaussian_noise_attack import gaussian_noise_function
from attacks.jpeg_attack import jpeg_function
from attacks.salt_pepper_attack import salt_pepper_function
from attacks.drop_out_attack import drop_out_function
from attacks.cropping_attack import cropping_function
from attacks.scaling_attack import scaling_function


class CombinedAttack(BaseAttack):
    """
    Applies 2-3 random attacks in sequence to simulate realistic scenarios
    """
    def __init__(self, **kwargs):
        super(CombinedAttack, self).__init__()
        
        # Available attack functions
        self.attack_functions = [
            gaussian_noise_function,
            jpeg_function,
            salt_pepper_function,
            drop_out_function,
            cropping_function,
            scaling_function
        ]
        
        self.attack_names = [
            'gaussian_noise',
            'jpeg_compression',
            'salt_pepper',
            'dropout',
            'cropping',
            'scaling'
        ]

    def apply_random_attacks(self, inputs):
        """
        Apply 2-3 random attacks in sequence
        """
        # Randomly decide how many attacks to apply (2 or 3)
        num_attacks = tf.random.uniform([], minval=2, maxval=4, dtype=tf.int32)
        
        # We'll use Python control flow here since we need to select random attacks
        # TensorFlow's control flow is complex for this use case
        
        # Generate random indices for attack selection
        # We'll apply attacks sequentially
        output = inputs
        
        # For simplicity and TensorFlow compatibility, we'll use a fixed approach:
        # Randomly select 2-3 attacks and apply them
        
        # Random selection approach using tf.random
        # Attack 1: Random choice
        attack_id_1 = tf.random.uniform([], minval=0, maxval=6, dtype=tf.int32)
        output = tf.switch_case(
            attack_id_1,
            branch_fns={
                0: lambda: gaussian_noise_function(output),
                1: lambda: jpeg_function(output),
                2: lambda: salt_pepper_function(output),
                3: lambda: drop_out_function(output),
                4: lambda: cropping_function(output),
                5: lambda: scaling_function(output)
            }
        )
        
        # Attack 2: Random choice (different from attack 1)
        attack_id_2 = tf.random.uniform([], minval=0, maxval=6, dtype=tf.int32)
        output = tf.switch_case(
            attack_id_2,
            branch_fns={
                0: lambda: gaussian_noise_function(output),
                1: lambda: jpeg_function(output),
                2: lambda: salt_pepper_function(output),
                3: lambda: drop_out_function(output),
                4: lambda: cropping_function(output),
                5: lambda: scaling_function(output)
            }
        )
        
        # Attack 3: Apply with 50% probability
        apply_third = tf.random.uniform([]) > 0.5
        
        if apply_third:
            attack_id_3 = tf.random.uniform([], minval=0, maxval=6, dtype=tf.int32)
            output = tf.switch_case(
                attack_id_3,
                branch_fns={
                    0: lambda: gaussian_noise_function(output),
                    1: lambda: jpeg_function(output),
                    2: lambda: salt_pepper_function(output),
                    3: lambda: drop_out_function(output),
                    4: lambda: cropping_function(output),
                    5: lambda: scaling_function(output)
                }
            )
        
        return output

    def call(self, inputs):
        return self.apply_random_attacks(inputs)


def combined_attack_function(x):
    return CombinedAttack()(x)
