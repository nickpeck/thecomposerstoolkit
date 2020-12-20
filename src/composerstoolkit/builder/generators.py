from ..core import CTEvent, CTGenerator

@CTGenerator
def cantus(list_pitches=[]):
    return [CTEvent(p, 0) for p in list_pitches]
    
@CTGenerator
def steady_pulse(ticks=0, n_pulses=1):
    return[CTEvent(None, ticks) for i in range(n_pulses)]
    
@CTGenerator
def collision_pattern(x, y):
    """given clocks in the ratio x:y , 
    generate the sequence of attack points 
    that results from the colision of their pulses.
    For example, given clocks 200 & 300, the resulting 
    sequence of (pitch,duration) events would be:
    
    [(None, 200),(None, 100),(None, 100),(None, 200)]
    """
    if x == y:
        return [CTEvent(None, x)]
    n_ticks = x * y
    pulse_pattern = [0 for i in range(0, n_ticks)]
    for i in range(0, n_ticks):
        if i % x == 0 or i % y == 0:
            pulse_pattern[i] = 1
    
    durations = []
    cur_duration = None
    
    for i in range(n_ticks -1):
        current = pulse_pattern[i]
        
        if current is 1:
            if cur_duration is not None:
                durations.append(cur_duration)
            cur_duration = 1
        elif current is 0:
            cur_duration = cur_duration + 1
    durations.append(cur_duration + 1)
    
    return [CTEvent(None, d) for d in durations]