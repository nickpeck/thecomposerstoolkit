import unittest

from composerstoolkit import (CTEvent, CTSequence, CTGenerator,
chain, NotChainableException, midievent, Container, permutate)

class CTEventTests(unittest.TestCase):
    
    def test_ctevent_defaults(self):
        cte = CTEvent()
        assert cte.pitches == []
        assert cte.duration == 0
        
    def test_ctevent_str(self):
        cte = CTEvent()
        assert str(cte) == "<CTEvent [], 0>"
        
    def test_ctevent_creation(self):
        cte = CTEvent(3, 400)
        assert cte.pitches == [3]
        assert cte.duration == 400
        
    def test_setattr_raises_exc(self):
        cte = CTEvent()
        with self.assertRaises(NotImplementedError) as context:
            cte.pitch = 5
            
    def test_delattr_raises_exc(self):
        cte = CTEvent()
        with self.assertRaises(NotImplementedError) as context:
            del cte.pitch
        
    def test_ctevent_addition(self):
        cte1 = CTEvent(1,600)
        cte2 = CTEvent(3,400)
        seq = cte1 + cte2
        assert seq.events == [cte1, cte2]
        
    def test_equality(self):
        cte1 = CTEvent(1,600)
        cte2 = CTEvent(1,600)
        assert cte1 == cte2
        assert cte1 is not cte2
    
    def test_inequality(self):
        cte1 = CTEvent(1,600)
        cte2 = CTEvent(2,400)
        assert cte1 != cte2
    
    
class CTSequenceTests(unittest.TestCase):
    
    def test_sequence_creation(self):
        cts = CTSequence([CTEvent(62,100)])
        assert cts.memento == None
        assert cts.events == [CTEvent(62,100)]
        
    def sequence(self):
        cts = CTSequence([CTEvent(62,100)])
        assert str(cts) == "<CTSequence [CTEvent(62,100)]>"
        
    def test_sequence_can_be_chained(self):
        cts = CTSequence([CTEvent(62,100)])
        
        def test_modifier(sequence):
            result = []
            for e in sequence.events:
                new_pitches = [p * 2 for p in e.pitches]
                result.append(CTEvent(new_pitches,  e.duration * 2))
            return result
        
        new_seq = cts.chain(test_modifier)
        assert new_seq.events == [CTEvent(124,200)]
        assert new_seq.memento == cts
    
    def test_chain_using_infix_syntax(self):
        cts = CTSequence([CTEvent(62,100)])
        
        def test_modifier(sequence):
            result = []
            for e in sequence.events:
                new_pitches = [p * 2 for p in e.pitches]
                result.append(CTEvent(new_pitches,  e.duration * 2))
            return result
        
        new_seq = cts |chain| test_modifier
        assert new_seq.events == [CTEvent([124],200)]
        assert new_seq.memento == cts
    
    def test_chain_using_infix_raises_exc_if_not_chainable(self):
        not_chainable = [CTEvent(62,100)]
        
        def test_modifier(sequence): pass
        
        with self.assertRaises(NotChainableException) as context:
            new_seq = not_chainable |chain| test_modifier
            
    def test_sequence_is_slicable(self):
        cts = CTSequence([
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100)])
            
        sliced = cts[0]        
        assert sliced.events == [CTEvent(60,100)]
        sliced_middle = cts[1]        
        assert sliced_middle.events == [CTEvent(62,100)]
        sliced_end = cts[3]        
        assert sliced_end.events == [CTEvent(60,100)]
        
        sliced_head = cts[:1]
        assert sliced_end.events == [CTEvent(60,100)]
        sliced_tail = cts[1:]
        assert sliced_tail.events == [
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100)]
            
        sliced_portion = cts[0:3]
        assert sliced_portion.events == [
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100)]
            
        sliced_with_step = cts[0:3:2]
        assert sliced_with_step.events == [
            CTEvent(60,100),
            CTEvent(64,100)]
            
    def test_to_midi_events(self):
        cts = CTSequence([
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100)])
            
        midi = cts.to_midi_events()
        assert midi == [
            midievent(pitch=60, type="NOTE_ON", time=0),
            midievent(pitch=60, type="NOTE_OFF", time=100),
            midievent(pitch=62, type="NOTE_ON", time=100),
            midievent(pitch=62, type="NOTE_OFF", time=200),
            midievent(pitch=64, type="NOTE_ON", time=200),
            midievent(pitch=64, type="NOTE_OFF", time=300),
            midievent(pitch=60, type="NOTE_ON", time=300),
            midievent(pitch=60, type="NOTE_OFF", time=400)]
            
    def test_lookup(self):
        cts = CTSequence([
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100)])
            
        assert cts.lookup(-1) == None
        assert cts.lookup(0) == CTEvent(60,100)
        assert cts.lookup(50) == CTEvent(60,100)
        assert cts.lookup(99) == CTEvent(60,100)
        assert cts.lookup(100) == CTEvent(60,100)
        assert cts.lookup(101) == CTEvent(62,100)
        assert cts.lookup(400) == CTEvent(60,100)
        assert cts.lookup(401) == None
        
    def test_sequence_to_pitch_Set(self):
        cts = CTSequence([
            CTEvent(67,100),
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100)])
        assert cts.to_pitch_set() == {60,62,64,67}
       
    def test_sequence_to_pitch_class_Set(self):
        cts = CTSequence([
            CTEvent(67,100),
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100)])
        assert cts.to_pitch_class_set() == {0,2,4,7}
       
    def test_get_pitches_and_durations(self):
        cts = CTSequence([
            CTEvent(67,100),
            CTEvent(60,100),
            CTEvent(62,200),
            CTEvent(64,100),
            CTEvent(60,100)])
            
        assert cts.pitches == [67,60,62,64,60]
        assert cts.durations == [100,100,200,100,100]
       
class PermutationsTests(unittest.TestCase):
    
    def test_permutate_single_generations(self):
        assert permutate([2,1,1,2]) == [
            (1, 2, 1, 2), 
            (1, 1, 2, 2), 
            (2, 1, 2, 1), 
            (2, 2, 1, 1), 
            (2, 1, 1, 2), 
            (1, 2, 2, 1)]
    
    def test_permutate_multiple_generations(self):
        assert permutate([2,1,1,2], 2) == [
            (1, 2, 1, 2), 
            (1, 1, 2, 2), 
            (2, 1, 2, 1), 
            (2, 2, 1, 1), 
            (2, 1, 1, 2), 
            (1, 2, 2, 1),
            (1, 1, 1, 1, 1, 1)]
        # True indicates to return the last generation only:
        assert permutate([2,1,1,2], 2, True) == [(1, 1, 1, 1, 1, 1)]
        assert permutate([4,5], 3) == [
            (1, 2, 1, 1, 1, 1, 1, 1), (5, 4), 
            (2, 3, 2, 2), (2, 2, 3, 2), 
            (1, 1, 1, 1, 2, 1, 1, 1), 
            (2, 1, 1, 1, 1, 1, 1, 1), (4, 5), 
            (1, 1, 1, 1, 1, 1, 2, 1), 
            (1, 1, 1, 1, 1, 1, 1, 2), (3, 2, 2, 2), 
            (1, 1, 1, 1, 1, 2, 1, 1), 
            (1, 1, 1, 2, 1, 1, 1, 1), 
            (1, 1, 2, 1, 1, 1, 1, 1), (2, 2, 2, 3)]
    
class CTGeneratorTests(unittest.TestCase):
    
    def test_ctgenerator_returns_sequence(self):
        my_functor = lambda :  [CTEvent(60,100), CTEvent(62,50)]
        my_generator = CTGenerator(my_functor)
        new_seq = my_generator()
        assert new_seq.memento == None
        assert new_seq.events == [CTEvent(60,100), CTEvent(62,50)]
        
    def test_ctgenerator_creation_decorator(self):
        @CTGenerator
        def my_functor(pitch, duration, n_events):
            return [CTEvent(pitch,duration) for i in range(n_events)]
        
        new_seq = my_functor(64,400,3)
        assert new_seq.memento == None
        assert new_seq.events == [CTEvent(64,400), CTEvent(64,400), CTEvent(64,400)]
        
class ContainerTests(unittest.TestCase):
    
    def test_build_container(self):
        container = Container()
        cts = CTSequence([
            CTEvent(60,100),
            CTEvent(62,100)])
            
        container.add_sequence(0, cts)
        events = container.get_playback_events()
        assert events[0] == midievent(pitch=60, type='NOTE_ON', time=0)
        assert events[1] == midievent(pitch=60, type='NOTE_OFF', time=100)
        assert events[2] == midievent(pitch=62, type='NOTE_ON', time=100)
        assert events[3] == midievent(pitch=62, type='NOTE_OFF', time=200)
        
    def test_w_offset(self):
        container = Container()
        cts = CTSequence([
            CTEvent(60,100),
            CTEvent(62,100)])
            
        container.add_sequence(100, cts)
        events = container.get_playback_events()
        assert events == [
            midievent(pitch=60, type='NOTE_ON', time=100),
            midievent(pitch=60, type='NOTE_OFF', time=200),
            midievent(pitch=62, type='NOTE_ON', time=200),
            midievent(pitch=62, type='NOTE_OFF', time=300)]
        
    def test_two_channels_offset(self):
        container = Container()
        cts1 = CTSequence([
            CTEvent(60,100),
            CTEvent(62,100)])
            
        cts2 = CTSequence([
            CTEvent(60,100),
            CTEvent(55,100)])
            
        container.add_sequence(0, cts1)
        container.add_sequence(50, cts2)
        events = container.get_playback_events()
        assert events == [
            midievent(pitch=60, type='NOTE_ON', time=0),
            midievent(pitch=60, type='NOTE_ON', time=50),
            midievent(pitch=60, type='NOTE_OFF', time=100),
            midievent(pitch=62, type='NOTE_ON', time=100),
            midievent(pitch=60, type='NOTE_OFF', time=150),
            midievent(pitch=55, type='NOTE_ON', time=150),
            midievent(pitch=62, type='NOTE_OFF', time=200),
            midievent(pitch=55, type='NOTE_OFF', time=250)]