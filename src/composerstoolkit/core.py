from collections import namedtuple
import itertools
from time import sleep

from midiutil.MidiFile import MIDIFile
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

_ctevent = namedtuple("ctevent", ["pitches", "duration"])

class CTEvent(_ctevent):
    
    def __new__(cls, pitches=None, duration=0):
        if pitches is None:
            pitches = []
        elif isinstance(pitches, int):
            pitches = [pitches]
        return _ctevent.__new__(cls, pitches, duration)
    
    @property
    def pitches(self):
        return self[0]
    
    @property
    def duration(self):
        return self[1]
    
    def __str__(self):
        return "<CTEvent {0}, {1}>".format(self.pitches, self.duration)
    
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
            for pitch in e.pitches:
                results.append(midievent(
                    pitch = pitch,
                    type = "NOTE_ON",
                    time = time_offset
                ))
                results.append(midievent(
                    pitch = pitch,
                    type = "NOTE_OFF",
                    time = time_offset + e.duration
                ))
            time_offset = time_offset + e.duration
        results.sort(key=lambda x: x.time, reverse=False)
        return results
        
    @property
    def pitches(self):
        return list(itertools.chain.from_iterable([e.pitches for e in self.events]))
    
    @property
    def durations(self):
        return [e.duration for e in self.events]
        
    def to_pitch_set(self):
        return {* (itertools.chain.from_iterable([e.pitches for e in self.events]))}
        
    def to_pitch_class_set(self):
        pitch_set = self.to_pitch_set()
        return {*[p % 12 for p in pitch_set]}
        
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
        
    def __add__(self, other):
        events = self.events[:] + other.events[:]
        return CTSequence(events)
    
    
def CTGenerator(functor):
    def getConfig(*args, **kwargs):
        return CTSequence(functor(*args, **kwargs))
    return getConfig
    
import functools
class reprwrapper(object):
    """helper to override __repr__ for a function for debugging purposes
    see https://stackoverflow.com/questions/10875442/possible-to-change-a-functions-repr-in-python
    """
    def __init__(self, repr, func):
        self._repr = repr
        self._func = func
        functools.update_wrapper(self, func)
    def __call__(self, *args, **kw):
        return self._func(*args, **kw)
    def __repr__(self):
        return self._repr(self._func)
        
def withrepr(reprfun):
    """decorator for reprwrapper"""
    def _wrap(func):
        return reprwrapper(reprfun, func)
    return _wrap
    
class CTTransformer():
    
    def __init__(self, functor):
        self._functor = functor
    
    def __call__(self, *args, **kwargs):
        @withrepr(
            lambda x: "<CTTransformer: {}{}>".format(
                self._functor.__name__, args + tuple(kwargs.items())))
        def transform(instance):
            nonlocal args
            nonlocal kwargs
            _kwargs = kwargs
            if "gate" in kwargs.keys():
                gate = _kwargs["gate"]
                del _kwargs["gate"]
                _args = args[:]
                return gate(self._functor, instance, *_args, **_kwargs)
            _args = [instance] + list(args)
            return self._functor(*_args, **_kwargs)
        return transform
    
    def __str__(self):
        return "<CTTransformer : {}>".format(self._functor.__name__)
    
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
            
            if cur_gate_event is None:
                # # there is no event at this offset
                # # just append 'e' to result
                buffer = buffer + [e]
                past_toggle_state = False
                continue
            
            cur_toggle_state = (cur_gate_event.pitches != [])
            has_changed = cur_toggle_state != past_toggle_state
            
            if not has_changed or i == 0:
                # no change, just add to the buffer
                buffer = buffer + [e]
            
            elif has_changed and cur_toggle_state:
                # the gate has changed to 'on'
                # add the buffer to result
                result = result + buffer
                buffer = [e]
            
            elif has_changed and not cur_toggle_state and i:
                # the gate has changed to 'off'
                # transform the contents of buffer
                _args = [CTSequence(buffer)] + list(args)
                buffer = functor(*_args, **kwargs)
                # add to result
                result = result + buffer
                buffer = [e]
                
            past_toggle_state = cur_toggle_state

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
        return result
    return transform
    
    
class Container():
    def __init__(self,  **kwargs):
        self.options = {
            "bpm": 120,
            "playback_rate": 1
        }
        self.sequences = []
        self.options.update(kwargs)
        
    def add_sequence(self, offset, seq, channel_no=None):
        if channel_no is None:
            channel_no = len(self.sequences)
        self.sequences.append((channel_no, offset, seq))
        
    def get_playback_events(self):
        playback_rate = self.options["playback_rate"]
        all_midi_events = []
        for (channel_no, offset,seq) in self.sequences:
            for me in seq.to_midi_events(offset):
                all_midi_events.append(midievent(me.pitch, me.type, me.time / playback_rate))
        all_midi_events = sorted(all_midi_events, key=lambda x: x.time)
        return all_midi_events
        
    def playback(self, player_func, dynamic=60):
        playback_events = self.get_playback_events()
        #nb the events are chronologically ordered
        count = 0
        for event in playback_events:
            if event.time != count:
                sleep(event.time - count)
            count = event.time
            if event.type == "NOTE_ON":
                player_func.noteon(0, event.pitch, dynamic)
            elif event.type == "NOTE_OFF":
                player_func.noteoff(0, event.pitch)
                
    def save_as_midi_file(self, filename, dynamic=60):
        mf = MIDIFile(len(self.sequences))
        for (channel_no, offset, seq) in self.sequences:
            mf.addTrackName(channel_no, offset, "Channel {}".format(channel_no))
            count = offset
            for event in seq.events:
                for pitch in event.pitches:
                    mf.addNote(channel_no, 0, pitch, count, event.duration, dynamic)
                count = count + event.duration
        # mf.addTempo(0, 0, self.options["bpm"])
        with open(filename, 'wb') as outf:
            mf.writeFile(outf)
        
class Vertex(object):
    """
    Vertex used to represent a musical event when parsed into 
    a directed graph structure
    """
    @classmethod
    def treeFromGraph(cls, graph):
        results = {}
        for key in graph.keys():
            v = Vertex(key)
            results[key] = v
        for key in graph.keys():
            node = results[key]
            neighbours = graph[key]
            for (name, pitch_delta, time_delta) in neighbours:
                try:
                    neighbour = results[name]
                except KeyError:
                    results[name] = Vertex(name)
                node.addNeighbour((pitch_delta, time_delta), results[name])
        return [v for k,v in results.items()]
                
    def __init__(self, name):
        self.name = name
        self.neighbours = []
        
    def __repr__(self):
        return "Vertex({})".format(self.name)
        
    def addNeighbour(self, vector, neighbour):
        self.neighbours.append((vector, neighbour))