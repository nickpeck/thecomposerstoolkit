import unittest

from composerstoolkit.core import CTEvent, CTSequence, CTGenerator, chain, NotChainableException

class CTEventTests(unittest.TestCase):
    
    def test_ctevent_defaults(self):
        cte = CTEvent()
        assert cte.pitch == None
        assert cte.duration == 0
        
    def test_ctevent_str(self):
        cte = CTEvent()
        assert str(cte) == "<MuseEvent None, 0>"
        
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
        assert cts.previous_states == []
        assert cts.events == [CTEvent(62,100)]
        
    def test_sequence_can_be_chained(self):
        cts = CTSequence([CTEvent(62,100)])
        
        def test_modifier(sequence):
            return [CTEvent(e.pitch * 2 , e.duration * 2) 
                for e in sequence.events] 
        
        new_seq = cts.chain(test_modifier)
        assert new_seq.events == [CTEvent(124,200)]
        assert new_seq.previous_states == [[CTEvent(62,100)]]
    
    def test_chain_using_infix_syntax(self):
        cts = CTSequence([CTEvent(62,100)])
        
        def test_modifier(sequence):
            return [CTEvent(e.pitch * 2 , e.duration * 2) 
                for e in sequence.events] 
        
        new_seq = cts |chain| test_modifier
        assert new_seq.events == [CTEvent(124,200)]
        assert new_seq.previous_states == [[CTEvent(62,100)]]
    
    def test_chain_using_infix_raises_exc_if_not_chainable(self):
        not_chainable = [CTEvent(62,100)]
        
        def test_modifier(sequence): pass
        
        with self.assertRaises(NotChainableException) as context:
            new_seq = not_chainable |chain| test_modifier
    
    
class CTGeneratorTests(unittest.TestCase):
    
    def test_ctgenerator_returns_sequence(self):
        my_functor = lambda :  [CTEvent(60,100), CTEvent(62,50)]
        my_generator = CTGenerator(my_functor)
        new_seq = my_generator()
        assert new_seq.previous_states == []
        assert new_seq.events == [CTEvent(60,100), CTEvent(62,50)]
        
    def test_ctgenerator_creation_decorator(self):
        @CTGenerator
        def my_functor(pitch, duration, n_events):
            return [CTEvent(pitch,duration) for i in range(n_events)]
        
        new_seq = my_functor(64,400,3)
        assert new_seq.previous_states == []
        assert new_seq.events == [CTEvent(64,400), CTEvent(64,400), CTEvent(64,400)]