from collections import namedtuple

from toolz import pipe as pipe
from infix import or_infix

class NotChainableException(Exception): pass

@or_infix
def chain(a,b):
    try:
        return a.chain(b)
    except AttributeError:
        raise NotChainableException(
            "object {} is not chainable".format(str(a)))

_ctevent = namedtuple("ctevent", ["pitch", "duration"])

class CTEvent(_ctevent):
    
    def __new__(cls, pitch=None, duration=0):
        return _ctevent.__new__(cls, pitch, duration)
    
    @property
    def pitch(self):
        return self[0]
    
    @property
    def duration(self):
        return self[1]
    
    def __str__(self):
        return "<MuseEvent {0}, {1}>".format(self.pitch, self.duration)
        
    def __add__(self, other):
        return CTSequence([self, other])
    
    def __setattr__(self, *ignored):
        raise NotImplementedError
    
    def __delattr__(self, *ignored):
        raise NotImplementedError
    
    
_midievent = namedtuple("midievent", ["pitch", "dynamic", "timeoffset"])
    
class CTSequence():
    
    def __init__(self, events, previous_states=[]):
        self.events = events
        self.previous_states = previous_states
    
    def chain(self, f):
        _states = self.previous_states[:]
        _states.append(self.events)
        new_events = f(self)
        return CTSequence(new_events, _states)
        
    def to_midi_events(self, time_offset=0):
        raise NotImplementedError
    
    
def CTGenerator(functor):
    def getConfig(*args, **kwargs):
        return CTSequence(functor(*args, **kwargs))
    return getConfig
    
    
class CTTransformer():
    
    def __init__(self, functor):
        self._functor = functor
    
    def call(self, *args, **kwargs):
        def transform(instance):
            args = [instance] + args
            return self._functor(*args, **kwargs)
        return inner