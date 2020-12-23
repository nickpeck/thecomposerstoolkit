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
        return "<CTEvent {0}, {1}>".format(self.pitch, self.duration)
        
    def __add__(self, other):
        return CTSequence([self, other])
    
    def __setattr__(self, *ignored):
        raise NotImplementedError
    
    def __delattr__(self, *ignored):
        raise NotImplementedError
    
    
midievent = namedtuple("midievent", ["pitch", "type", "time"])
    
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
        results = []
        for e in self.events:
            results.append(midievent(
                pitch = e.pitch,
                type = "NOTE_ON",
                time = time_offset
            ))
            results.append(midievent(
                pitch = e.pitch,
                type = "NOTE_OFF",
                time = time_offset + e.duration
            ))
            time_offset = time_offset + e.duration
        results.sort(key=lambda x: x.time, reverse=False)
        return results
        
    def lookup(self, offset=0):
        if offset < 0:
            return None
        for e in self.events:
            if e.duration >= offset:
                return e
            offset = offset - e.duration
        return None
        
    def __getitem__(self, slice):
        start, stop, step = None, None, None
        try:
            start, stop, step = slice
            sliced_events = self.events[start:stop:step]
        except TypeError:
            try:
                start, stop = slice
                sliced_events = self.events[start:stop]
            except TypeError:
                start = slice
                sliced_events = self.events[start]
                if not isinstance(sliced_events , list):
                    sliced_events = [sliced_events]
        
        _states = self.previous_states[:]
        _states.append(self.events)
        return CTSequence(sliced_events, _states)
    
    
def CTGenerator(functor):
    def getConfig(*args, **kwargs):
        return CTSequence(functor(*args, **kwargs))
    return getConfig
    
    
class CTTransformer():
    
    def __init__(self, functor):
        self._functor = functor
    
    def __call__(self, *args, **kwargs):
        def transform(instance):
            nonlocal args
            nonlocal kwargs
            args = [instance] + list(args)
            return self._functor(*args, **kwargs)
        return transform