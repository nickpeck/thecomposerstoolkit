import itertools
import math
import random

from composerstoolkit.core import (CTEvent, CTSequence)
from composerstoolkit.builder.generators import cantus
from composerstoolkit.resources import NOTE_MIN, NOTE_MAX

def random_walk(base_seq, mutators=[lambda x: x], 
    constraints=[lambda x: True], adjust_weights=True):
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
    ticks=0
    while True:
        mutating = True
        while mutating:
            # choose a random weighted transformation to apply

            mutator = random.choices(mutators, weights)[0]

            candidate = CTSequence(mutator(base_seq))
            context = (candidate, candidate, ticks)
            passed=True
            # test that the whole sequence meets the given constraints
            # cycle until we have a sequence that passes checks
            for c in constraints:
                if not c(context):
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
            ticks = ticks + 1
        res = base_seq[-1]
        yield res
    
class UnsatisfiableException(Exception): pass
    
def random_walk_backtracking(starting_pitch=60, 
        n_events=64, constraints=[lambda x: True]):
    """Extend a given pitch sequence  by up to n_events, using
    an unweighted random selection process and backtracking solver.
    
    seed - CTEvent (starting pitch)
    n_events - how long to make the target sequence
    constraints - a list of constraints that should be satisfied at each stage. If the 
        transformation fails to meet the constraints, it will be rejected and the solver
        will backtrack to select a new path. 'Dead' paths are tracked and rejected.
        Each constraint recieves a tuple of (note, seq, tick), where tick is the number
        of the event.
    
    returns: CTSequence or UnsatisfiableException if a solution that satisfies the
        constraints cannot be found.
        
    """
    tick = 0
    seq = [starting_pitch]
    if n_events == 1:
        return cantus(seq)
    choices = list(range(NOTE_MIN, NOTE_MAX))
    dead_paths = []
    while tick < n_events-1:
        # lets use a very basic random choice to begin with and see how far we go
        try:
            note = random.choice(choices)
        except IndexError:
            # this was thrown because we ran out of choices (we have reached a dead-end)
            # so you back-track... do it again....
            dead_paths.append(seq[:])
            seq = seq[:-1]
            tick = tick -1
            choices = list(range(NOTE_MIN, NOTE_MAX))
            if tick == 0:
                raise UnsatisfiableException("Unable to solve!")
                break
            else:
                continue
        context = (note, cantus(seq + [note]), tick)
        results = set()
        for constraint in constraints:
            results.update([constraint(context)])
        candidate = seq[:]
        candidate.append(note)
        if results == {True} and candidate not in dead_paths:
            seq.append(note)
            tick = tick + 1
            choices = list(range(NOTE_MIN, NOTE_MAX))
        else:
            #this choice was bad, so we must exclude it
            choices.remove(note)
    return cantus(seq)
    
    
def random_walk_backtracking_w_heuristics(starting_pitch=60,
        n_events=8, constraints=[lambda x: True], 
        heuristics=[lambda context,choices,weights: weights]):
    tick = 0
    seq = [starting_pitch]
    if n_events == 1:
        return cantus(seq)
    choices = list(range(NOTE_MIN, NOTE_MAX))
    dead_paths = []
    while tick < n_events-1:
        # lets use a very basic random choice to begin with and see how far we go
        weights= [1.0 for i in range(len(choices))]
        for heuristic in heuristics:
            weights = heuristic(tick, choices, weights)
        try:
            note = random.choices(choices, weights)[0]
        except IndexError:
            # this was thrown because we ran out of choices (we have reached a dead-end)
            # so you back-track... do it again....
            dead_paths.append(seq[:])
            seq = seq[:-1]
            tick = tick -1
            choices = list(range(NOTE_MIN, NOTE_MAX))
            if tick == 0:
                raise UnsatisfiableException("Unable to solve!")
                break
            else:
                continue
        context = (note, cantus(seq + [note]), tick)
        results = set()
        for constraint in constraints:
            results.update([constraint(context)])
        candidate = seq[:]
        candidate.append(note)
        if results == {True} and candidate not in dead_paths:
            seq.append(note)
            tick = tick + 1
            choices = list(range(NOTE_MIN, NOTE_MAX))
        else:
            #this choice was bad, so we must exclude it
            choices.remove(note)
    return cantus(seq)
    pass