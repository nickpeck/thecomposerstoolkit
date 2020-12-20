import math

from ..core import CTEvent, CTTransformer

@CTTransformer
def loop(seq, n_times=1):
    if n_times < 0:
        raise ValueError("n_times cannot be less than 0")
    result = []
    for i in range(n_times):
        result = result + seq.events
    return result
    
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
    events = seq.events[:]
    events.reverse()
    return events
    
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
    if seq.events == []:
        return []
    rotated = seq.events[:]
    for i in range(no_times):
        rotated = rotated[1:] + [rotated[0]]
    return rotated
    
@CTTransformer
def mutation(seq, threshold=0.5, transformations=[], constraints=[]):
    raise NotImplementedError
    
@CTTransformer
def linear_interpolate(seq, resolution=1):
    raise NotImplementedError
    
@CTTransformer
def explode_intervals(seq, factor, mode="exponential"):
    events = seq.events[:]
    if len(events) is 1:
        return events
    
    def _vectors(seq):
        vectors = []
        x = seq.events[0]
        for y in seq.events[1:]:
            vectors.append(y.pitch-x.pitch)
            x = y
        return vectors
    
    if mode == "exponential":
        interval_vectors = [(factor * v)for v in _vectors(seq)]
    elif mode == "linear":
        interval_vectors = [(factor + v) for v in _vectors(seq)]
    else:
        raise Exception("unrecognised mode "+ mode)
    
    # first item in the seq stays as-is
    i_events = iter(seq.events)
    i_vectors = iter(interval_vectors)
    result = [next(i_events)]
    # apply the interval_vectors to distort the remaining items
    pitch = result[0].pitch
    while True:
        try:
            next_event = next(i_events)
            next_vector = next(i_vectors)
            pitch = math.ceil(next_vector + pitch)
            result.append(CTEvent(pitch, next_event.duration))
        except StopIteration:
            break
    return result
    
@CTTransformer
def rhythmic_augmentation(seq, multiplier):
    return [CTEvent(e.pitch, multiplier*e.duration) for e in seq.events]
    
@CTTransformer
def rhythmic_diminution(seq, factor):
    return [CTEvent(e.pitch, e.duration/factor) for e in seq.events]
    
