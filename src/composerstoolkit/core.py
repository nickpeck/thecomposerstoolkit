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
    
    def __init__(self, events, memento=None):
        self.events = events
        self.memento = memento
    
    def chain(self, f):
        new_events = f(self)
        return CTSequence(new_events, self)
        
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
        
        return CTSequence(sliced_events, self)
        
    def __str__(self):
        return "<CTSequence {}>".format(self.events)
    
    
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
            if "gate" in kwargs.keys():
                gate = kwargs["gate"]
                del kwargs["gate"]
                return gate(self._functor, instance, *args, **kwargs)
            args = [instance] + list(args)
            return self._functor(*args, **kwargs)
        return transform
    
def boolean_gate(gate):
    def transform(functor, instance, *args, **kwargs):
        nonlocal gate
        offset = 0
        result = []
        buffer = [] #toggle state, sequence
        past_toggle_state = False
        for i in range(len(instance.events)):
            e = instance.events[i]
            offset = offset + e.duration
            cur_gate_event = gate.lookup(offset)
            # print("-"*20)
            # print("result", result)
            # print("buffer", buffer)
            # print("cur_gate_event", cur_gate_event)
            
            if cur_gate_event is None:
                # print("GOT HERE ONE")
                # # there is no event at this offset
                # # just append 'e' to result
                buffer = buffer + [e]
                past_toggle_state = False
                continue
            
            cur_toggle_state = (cur_gate_event.pitch is not None)
            has_changed = cur_toggle_state != past_toggle_state
            # print("cur_toggle_state", cur_toggle_state)
            # print("past_toggle_state", past_toggle_state)
            
            if not has_changed or i == 0:
                # print("GOT HERE TWO")
                # no change, just add to the buffer
                buffer = buffer + [e]
            
            elif has_changed and cur_toggle_state:
                # print("GOT HERE THREE")
                # the gate has changed to 'on'
                # add the buffer to result
                result = result + buffer
                buffer = [e]
            
            elif has_changed and not cur_toggle_state and i:
                # print("GOT HERE FOUR")
                # the gate has changed to 'off'
                # transform the contents of buffer
                _args = [CTSequence(buffer)] + list(args)
                buffer = functor(*_args, **kwargs)
                # add to result
                result = result + buffer
                buffer = [e]
                
            past_toggle_state = cur_toggle_state


            # print("     buffer", buffer)
            # print("     result", result)
        # terminal condition
        if len(buffer) and cur_toggle_state:
            # there are items left in the buffer
            # state is ON is transform and add to result
            _args = [CTSequence(buffer)] + list(args)
            buffer = functor(*_args, **kwargs)
            # no transform, just add to result
            result = result + buffer
        if len(buffer) and not cur_toggle_state:
            # add to result
            result = result + buffer
        # print("END ", result)
        return result
    return transform