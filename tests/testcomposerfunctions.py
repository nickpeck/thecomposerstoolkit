import unittest

from composerstoolkit.core import (CTEvent, CTSequence, CTGenerator, CTTransformer)
from composerstoolkit.composers.solvers import random_loop_transformation
from composerstoolkit.builder.transformers import transpose
from composerstoolkit.composers.constraints import constraint_in_set

class SolversTests(unittest.TestCase):
    
    def test_random_loop_transformation(self):
        """Simple test of growing a sequence using a 
        single operation
        """
        base_seq = CTSequence([
            CTEvent(60,100),
        ])
        
        solver = random_loop_transformation(
            base_seq,
            [(transpose(1), 1)]
        )
        
        evt1 = next(solver)
        assert evt1.pitches[0] == 61
        evt2 = next(solver)
        assert evt2.pitches[0] == 62
        
    def test_random_loop_transformation_w_constraints(self):
    
        base_seq = CTSequence([
            CTEvent(70,100),
        ])
        
        target_note_range = set(list(range(60,80)))
        
        solver = random_loop_transformation(
            base_seq,
            # transformations dicate moving up or down in tones:
            [(transpose(2), 0.5), (transpose(-2), 0.5)],
            [constraint_in_set(target_note_range)]
        )
        # generate 100 items, and assert at each stage
        # that the overall sequence remains within the
        # specifed range
        for i in range(100):
            evt = next(solver)
            assert evt.pitches[0] in target_note_range