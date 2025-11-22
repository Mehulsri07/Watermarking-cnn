"""
Wrapper module for tensorflow_wavelets to provide WaveTFFactory interface
"""
from tensorflow_wavelets.Layers.DWT import DWT, IDWT


class WaveTFFactory:
    """Factory class for creating wavelet transform layers"""
    
    def build(self, wavelet_type='haar', dim=2, inverse=False):
        """
        Build a wavelet transform layer
        
        Args:
            wavelet_type: Type of wavelet (e.g., 'haar', 'db2')
            dim: Dimension of the transform (2 for 2D images)
            inverse: Whether to perform inverse transform
            
        Returns:
            A DWT or IDWT layer instance
        """
        if inverse:
            # splited=1 means input has 4 separate channels [ll, lh, hl, hh]
            return IDWT(wavelet_name=wavelet_type, splited=1)
        else:
            # concat=0 means output 4 channels [ll, lh, hl, hh]
            return DWT(wavelet_name=wavelet_type, concat=0)
