import unittest

from composerstoolkit.core import CTEvent, CTSequence, chain
from composerstoolkit.builder.transformers import loop, transpose, invert, retrograde



class CTLibraryTransformerTests(unittest.TestCase):
    
    def setUp(self):
        self.src = CTSequence([
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100),
        ])
    
    def test_loop(self):
        looped = self.src |chain| loop()
        assert looped.events == [
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100),
        ]
        
    def test_loop_twice(self):
        looped = self.src |chain| loop(2)
        assert looped.events == [
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100),
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100),
        ]
        
    def test_loop_raises_exp_negative_input(self):
        with self.assertRaises(ValueError) as context:
            looped = self.src |chain| loop(-1)
    
    def test_transpose(self):
        transposed = self.src |chain| transpose(1)
        assert transposed.events == [
            CTEvent(61,100),
            CTEvent(63,100),
            CTEvent(65,100),
            CTEvent(61,100),
        ]
        
    def test_transpose_down(self):
        transposed = self.src |chain| transpose(-1)
        assert transposed.events == [
            CTEvent(59,100),
            CTEvent(61,100),
            CTEvent(63,100),
            CTEvent(59,100),
        ]
        
    def test_invert(self):
        inverted = self.src |chain| invert()
        assert inverted.events == [
            CTEvent(60,100),
            CTEvent(58,100),
            CTEvent(56,100),
            CTEvent(60,100),
        ]
        
    def test_invert_specified_axis(self):
        inverted = self.src |chain| invert(62)
        assert inverted.events == [
            CTEvent(64,100),
            CTEvent(62,100),
            CTEvent(60,100),
            CTEvent(64,100),
        ]
        
    def test_invert_specified_axis_lower(self):
        inverted = self.src |chain| invert(59)
        assert inverted.events == [
            CTEvent(58,100),
            CTEvent(56,100),
            CTEvent(54,100),
            CTEvent(58,100),
        ]
        
    def test_retrograde(self):
        reversed = self.src |chain| retrograde()
        assert reversed.events == [
            CTEvent(60,100),
            CTEvent(64,100),
            CTEvent(62,100),
            CTEvent(60,100),
        ]