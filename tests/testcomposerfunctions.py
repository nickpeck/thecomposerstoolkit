import unittest

from composerstoolkit.core import (CTEvent, CTSequence, CTGenerator, CTTransformer)
from composerstoolkit.composers.solvers import random_loop_transformation
from composerstoolkit.builder.transformers import transpose
from composerstoolkit.composers.constraints import constraint_in_set

class SolversTests(unittest.TestCase):
    
    def test_random_loop_transformation(self):
        print("-----------",str(transpose(1)))
        base_seq = CTSequence([
            CTEvent(60,100),
        ])
        
        solver = random_loop_transformation(
            base_seq,
            [(transpose(1), 1)]
        )
        
        evt1 = next(solver)
        print(evt1)
        assert evt1.pitches[0] == 61
        evt2 = next(solver)
        print(evt2)
        assert evt2.pitches[0] == 62
        
    # def test_random_loop_transformation_w_constraints(self):
    
        # @CTTransformer
        # def no_transform(seq):
            # """Transpose all pitches in the 
            # given sequence by a constant interval.
            # """
            # result = seq.events[-1]
            # return result
    
        # base_seq = CTSequence([
            # CTEvent(70,100),
        # ])
        
        # target_note_range = range(60,80)
        
        # solver = random_loop_transformation(
            # base_seq,
            # [(transpose(5), 0.1), (no_transform(), 0.1)],
            # [constraint_in_set(target_note_range)]
        # )
        
        # for i in range(5):
            # evt = next(solver)
            # assert evt.pitches[0] in target_note_range