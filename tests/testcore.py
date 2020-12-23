import unittest

from composerstoolkit.core import (CTEvent, CTSequence, CTGenerator, 
chain, NotChainableException, midievent)

class CTEventTests(unittest.TestCase):
    
    def test_ctevent_defaults(self):
        cte = CTEvent()
        assert cte.pitch == None
        assert cte.duration == 0
        
    def test_ctevent_str(self):
        cte = CTEvent()
        assert str(cte) == "<CTEvent None, 0>"
        
    def test_ctevent_creation(self):
        cte = CTEvent(3, 400)
        assert cte.pitch == 3
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
        
    def test_sequence_can_be_chained(self):
        cts = CTSequence([CTEvent(62,100)])
        
        def test_modifier(sequence):
            return [CTEvent(e.pitch * 2 , e.duration * 2) 
                for e in sequence.events] 
        
        new_seq = cts.chain(test_modifier)
        assert new_seq.events == [CTEvent(124,200)]
        assert new_seq.memento == cts
    
    def test_chain_using_infix_syntax(self):
        cts = CTSequence([CTEvent(62,100)])
        
        def test_modifier(sequence):
            return [CTEvent(e.pitch * 2 , e.duration * 2) 
                for e in sequence.events] 
        
        new_seq = cts |chain| test_modifier
        assert new_seq.events == [CTEvent(124,200)]
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