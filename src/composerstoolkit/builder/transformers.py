from composerstoolkit.core import CTEvent, CTTransformer

@CTTransformer
def loop_sequence(seq, n_times=1):
    raise NotImplementedError
    
@CTTransformer
def transpose(seq, transposition):
    raise NotImplementedError
    
@CTTransformer
def retrograde(seq):
    raise NotImplementedError
    
@CTTransformer
def invert(seq, axis_pitch=None):
    raise NotImplementedError
    
@CTTransformer
def rotate(seq, no_times=1):
    raise NotImplementedError
    
@CTTransformer
def mutation(seq, threshold=0.5, transformations=[], constraints=[]):
    raise NotImplementedError
    
@CTTransformer
def linear_interpolate(seq, resolution=1):
    raise NotImplementedError
    
@CTTransformer
def explode(seq, factor, mode="exponential"):
    raise NotImplementedError