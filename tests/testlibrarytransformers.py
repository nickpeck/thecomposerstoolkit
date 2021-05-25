import unittest
    
from composerstoolkit import (CTEvent, CTSequence, chain, boolean_gate,
loop, transpose, invert, retrograde, rhythmic_augmentation, aggregate_into_chords,
rhythmic_diminution, explode_intervals, rotate, map_to_pulses, map_to_pitches)

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
        
    def test_transpose_multiple_invocations(self):
        functor = transpose(1)
        transposed1 = self.src |chain| functor
        transposed2 = transposed1 |chain| functor
        assert transposed2.events == [
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(66,100),
            CTEvent(62,100),
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
        
    def test_map_to_pulses(self):
        rhythm_seq = CTSequence([
            CTEvent(None,100),
            CTEvent(None,200),
            CTEvent(None,300),
        ])
        exploded = self.src |chain| map_to_pulses(rhythm_seq)
        assert exploded.events == [
            CTEvent(60,100),
            CTEvent(62,200),
            CTEvent(64,300)
        ]
        
    def test_map_to_pitches(self):
        rhythm_seq = CTSequence([
            CTEvent(None,100),
            CTEvent(None,200),
            CTEvent(None,300),
            CTEvent(None,400),
            CTEvent(None,500),
        ])
        exploded = rhythm_seq |chain| map_to_pitches(self.src)
        assert exploded.events == [
            CTEvent(60,100),
            CTEvent(62,200),
            CTEvent(64,300),
            CTEvent(60,400),
            CTEvent(None,500),
        ]
    
    # def test_linear_linear_interpolate(self):
        # interpolated = self.src |chain| linear_interpolate(2)
        # print(interpolated.events)
        
    def test_gated_transformer(self):
        input = CTSequence([
            CTEvent(60,100) for i in range(5)
        ])
        gate = CTSequence([
            CTEvent(1,100),
            CTEvent(None,100),
            CTEvent(1,100),
            CTEvent(None,100),
            CTEvent(1,100),
        ])
        transformed = input |chain| transpose(1, gate=boolean_gate(gate)) 
        assert transformed.events == [
            CTEvent(61,100),
            CTEvent(60,100),
            CTEvent(61,100),
            CTEvent(60,100),
            CTEvent(61,100),
        ]
        
    def test_gated_transformer_complex_gate_lengths(self):
        input = CTSequence([
            CTEvent(60,100) for i in range(6)
        ])
        gate = CTSequence([
            CTEvent(None,100),
            CTEvent(None,100),
            CTEvent(1,100),
            CTEvent(1,100),
            CTEvent(1,100),
            CTEvent(None,100),
        ])
        transformed = input |chain| transpose(1, gate=boolean_gate(gate)) 
        assert transformed.events == [
            CTEvent(60,100),
            CTEvent(60,100),
            CTEvent(61,100),
            CTEvent(61,100),
            CTEvent(61,100),
            CTEvent(60,100),
        ]
        
    def test_gated_transformer_zero_len_input(self):
        input = CTSequence([])
        gate = CTSequence([
            CTEvent(1,100),
            CTEvent(None,100),
            CTEvent(1,100),
            CTEvent(None,100),
            CTEvent(1,100),
        ])
        transformed = input |chain| transpose(1, gate=boolean_gate(gate)) 
        assert transformed.events == []
        
    def test_gated_transformer_gate_shorter_than_input(self):
        input = CTSequence([CTEvent(60,100) for i in range(5)])
        gate = CTSequence([
            CTEvent(1,100),
            CTEvent(None,100)
        ])
        transformed = input |chain| transpose(1, gate=boolean_gate(gate))
        assert transformed.events == [
            CTEvent(61,100),
            CTEvent(60,100),
            CTEvent(60,100),
            CTEvent(60,100),
            CTEvent(60,100),
        ]
        
    def test_i_can_compose_transformers(self):
        transformed = self.src.chain(transpose(1)).chain(transpose(1))
        assert transformed.events == [
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(66,100),
            CTEvent(62,100),
        ]
        
    def test_aggregate_into_chords(self):
        src = CTSequence([
            CTEvent(60,100),
            CTEvent(61,100),
            CTEvent(62,100),
            CTEvent(63,100),
            CTEvent(64,100),
            CTEvent(65,100),
            CTEvent(66,100),
            CTEvent(67,100),
        ])
        transformed = src.chain(aggregate_into_chords(3))
        assert transformed.events == [
            CTEvent([60, 61, 62], 1), 
            CTEvent([63, 64, 65], 1), 
            CTEvent([66, 67], 1)
        ]
