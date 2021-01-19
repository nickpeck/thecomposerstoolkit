import itertools
import math
import random

from composerstoolkit.core import (CTEvent, CTSequence)

def random_loop_transformation(base_seq, mutators=[lambda x: x], 
    constraints=[lambda x,y: True], adjust_weights=True):
    """Returns a generator function that grows a base sequence by performing
    a weighted random mutation to it
    
    base_seq - CTSequence instance
    threshold - float  (0.0 ...1.0) the chances that a transformation will occur
    mutators - a set of weighted CTTransformer instances that can be applied, these are
        expressed as [(t1, weight), (2, weight)...] or simply [t1, t2 ...]
    constraints - a list of constraints that should be satisfied at each stage. If the 
        transformation fails to meet the constraints, it will be rejected and a new
        transformation will be choosen. Can be empty.
    adjust_weights - boolean, if True, will increase the weighting of a mutator each time it
        is choosen and decrease the weighting each time it results in a failed outcome.
    """
    try:
        weights = [y for (x,y) in mutators]
        mutators = [x for (x,y) in mutators]
    except:
        weights = [1 for i in range(len(mutators))]
    while True:
        mutating = True
        context = {
            "previous" : base_seq
        }
        while mutating:
            # choose a random weighted transformation to apply

            mutator = random.choices(mutators, weights)[0]

            candidate = CTSequence(mutator(base_seq))
            passed=True
            # test that the whole sequence meets the given constraints
            # cycle until we have a sequence that passes checks
            for c in constraints:
                if not c(candidate, context):
                    passed = False
                    break
            if not passed:
                # adjust weights, negative bias
                if adjust_weights and weights[mutators.index(mutator)] > 0:
                    weights[mutators.index(mutator)] = weights[mutators.index(mutator)] - 0.1
                continue
            mutating = False
            
            base_seq = candidate
            # adjust weights, positive bias
            if adjust_weights and weights[mutators.index(mutator)] < 1:
                weights[mutators.index(mutator)] = weights[mutators.index(mutator)] + 0.1
        res =  base_seq[-1]
        yield res
    
def simple_constraints_backtracking_solver(seed=[60], length=64, constraints=[lambda x: True]):
    pass
    
    
def backtracking_solver_w_heuristics(seed=[60], length=64, constraints=[lambda x: True], heuristics=[lambda context,choices,weights: weights]):
    pass