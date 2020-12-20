import unittest

from composerstoolkit.core import CTEvent, CTSequence, chain
from composerstoolkit.builder.transformers import (loop, transpose, invert,
    retrograde, rhythmic_augmentation, rhythmic_diminution,
    explode_intervals, rotate)



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
            
    def test_empty_list(self):
        rotated = CTSequence([]) |chain| rotate()
        assert rotated.events == []
        
    def test_rotate(self):
        rotated = self.src |chain| rotate()
        assert rotated.events == [
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100),
            CTEvent(60,100),
        ]
    
    def test_rotate_2(self):
        rotated = self.src |chain| rotate(2)
        assert rotated.events == [
            CTEvent(64,100),
            CTEvent(60,100),
            CTEvent(60,100),
            CTEvent(62,100),
        ]
        
    def test_rotate_negative(self):
        rotated = self.src |chain| rotate(22)
        assert rotated.events == [
            CTEvent(64,100),
            CTEvent(60,100),
            CTEvent(60,100),
            CTEvent(62,100),
        ]
    
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
        
    def test_rhythmic_augmentation(self):
        augmented = self.src |chain| rhythmic_augmentation(2)
        assert augmented.events == [
            CTEvent(60,200),
            CTEvent(62,200),
            CTEvent(64,200),
            CTEvent(60,200),
        ]
        
    def test_rhythmic_diminution(self):
        compressed = self.src |chain| rhythmic_diminution(2)
        assert compressed.events == [
            CTEvent(60,50),
            CTEvent(62,50),
            CTEvent(64,50),
            CTEvent(60,50),
        ]
    
    def test_intervalic_explosion_exp(self):
        exploded = self.src |chain| explode_intervals(2)
        assert exploded.events == [
            CTEvent(60,100),
            CTEvent(64,100),
            CTEvent(68,100),
            CTEvent(60,100),
        ]
        
    def test_intervalic_explosion_linear(self):
        exploded = self.src |chain| explode_intervals(2, "linear")
        assert exploded.events == [
            CTEvent(60,100),
            CTEvent(64,100),
            CTEvent(68,100),
            CTEvent(66,100),
        ]
        
    def test_intervalic_explosion_single_event(self):
        exploded = self.src[0] |chain| explode_intervals(2, "linear")
        assert exploded.events == [CTEvent(60,100)]
        
    def test_intervalic_explosion_raised_exc_bad_mode(self):
        with self.assertRaises(Exception) as context:
            exploded = self.src |chain| explode_intervals(2, "---")
    
