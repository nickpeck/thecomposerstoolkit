from composerstoolkit.core import CTEvent, CTTransformer

@CTTransformer
def loop_sequence(seq, n_times=1):
    raise NotImplementedError
    
@CTTransformer
def transpose(seq, interval):
    """Transpose all pitches in the 
    given sequence by a constant interval.
    """
    result = []
    for evt in seq.events:
        result.append(
            CTEvent(
                evt.pitch + interval, 
                evt.duration))
    return result
    
@CTTransformer
def retrograde(seq):
    raise NotImplementedError
    
@CTTransformer
def invert(seq, axis_pitch=None):
    if axis_pitch is None:
        axis_pitch = seq.events[0].pitch
    res = []
    for evt in seq.events:
        delta = evt.pitch-axis_pitch
        if delta < 0: # note is below axis
            res.append(CTEvent(axis_pitch-delta, evt.duration))
        elif delta > 0: # note is above axis
            res.append(CTEvent(axis_pitch-delta, evt.duration))
        else: #its the axis, so stays the same
            res.append(CTEvent(evt.pitch, evt.duration))
    return res
    
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
def explode_intervals(seq, factor, mode="exponential"):
    raise NotImplementedError
    
@CTTransformer
def explode_durations(seq, factor, mode="exponential"):
    raise NotImplementedError
    
@CTTransformer
def rhythmic_augmentation(seq, factor):
    raise NotImplementedError
    
@CTTransformer
def rhythmic_diminution(seq, factor):
    raise NotImplementedError