import unittest

from composerstoolkit.core import CTEvent, CTSequence
from composerstoolkit.builder.generators import cantus, steady_pulse, collision_pattern

class CTLibraryGeneratorTests(unittest.TestCase):
    
    def test_cantus_defaults(self):
        seq = cantus()
        assert seq.events == []
        
    def test_cantus_simple(self):
        seq = cantus([0,2,4,0])
        assert seq.events == [
                CTEvent(0,0), 
                CTEvent(2,0), 
                CTEvent(4,0), 
                CTEvent(0,0)]
                
    def test_steady_pulse_defaults(self):
        seq = steady_pulse()
        assert seq.events == [CTEvent(None,0)]
        
    def test_steady_pulse_w_args(self):
        seq = steady_pulse(100, 4)
        assert seq.events == [
                CTEvent(None,100), 
                CTEvent(None,100), 
                CTEvent(None,100), 
                CTEvent(None,100)]
        
    def test_collision_pattern_basic(self):
        seq = collision_pattern(1,1)
        assert seq.events == [CTEvent(None,1)]
            
    def test_collision_pattern_3_over_2(self):
        seq = collision_pattern(3,2)
        assert seq.events == [
            CTEvent(None,2), 
            CTEvent(None,1), 
            CTEvent(None,1), 
            CTEvent(None,2)]
            
    def test_collision_pattern_400_over_500(self):
        seq = collision_pattern(4,5)
        assert seq.events == [
            CTEvent(None,4), 
            CTEvent(None,1), 
            CTEvent(None,3),
            CTEvent(None,2), 
            CTEvent(None,2), 
            CTEvent(None,3),
            CTEvent(None,1),
            CTEvent(None,4)]