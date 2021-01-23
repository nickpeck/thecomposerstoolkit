import itertools
import math
import random

from composerstoolkit.core import (CTSequence)
from composerstoolkit.builder.generators import cantus

class Extinction(Exception): pass

class Evolutionary():

    def __init__(self, **kwargs):
        """
        args:
        get_offspring (breed?)
        choose_parents
        fitness_func
        """
        try:
            self._fitness_func = kwargs["fitness_func"]
        except KeyError:unc = lambda seq: True
            
        try:
            self.transformations = kwargs["transformations"]
        except KeyError:
            self.transformations = []
            
        try:
            self.mutation_threshold = kwargs["mutation_threshold"]
        except KeyError:
            self.mutation_threshold = 0.1
            
        try:
            self._choose_parents_func = kwargs["choose_parents"]
        except KeyError:
            self._choose_parents_func = None
            
        try:
            self.debug = kwargs["debug"] == True
        except (TypeError, KeyError):
            self.debug = False
            
    
    def _breed(self, p1, p2=None):
        def f(seq):
            x = p1(seq)
            if p2 is None:
                return x
            y = p2(CTSequence(x))
            return y
        return f
        
    def _choose_parents(self, parents, weights):
        if self._choose_parents_func is not None:
            return self._choose_parents_func(parents, weights)
        if set(weights) == {0}:
            weights = [0.5 for p in parents]
        choice = random.choices(parents, weights)
        (trans1,w1) = choice[0]
        index = parents.index((trans1,w1))
        remaining_parents = parents[:]
        del remaining_parents[index]
        remaining_weights = weights[:]
        del remaining_weights[index]
        try:
            (trans2,w2) = random.choices(remaining_parents, remaining_weights)[0]
        except IndexError:
            (trans2,w2) = remaining_parents[0]
        return ((trans1,w1), (trans2,w2))
        
    def print_debug(self, *args):
        if self.debug:
            print(args)

    def __call__(self, base_seq=cantus([60]), n_events=8, debug=False):
        """Model of an evolutionary algorithm.
        """
        result = base_seq
        i = 0
        while i < n_events-1:
            self.print_debug("breeding cycle " + str(i))
            self.print_debug("n breeding types ", len(self.transformations))
            if len(self.transformations) <= 1:
                raise Extinction("There are not enough parents to continue, exiting")
            weights = [y for (x,y) in self.transformations]
            self.print_debug("weights:", weights)
            # a weighted random choice selects the 2 'fittest' parents:
            (trans1,w1), (trans2,w2) = self._choose_parents(self.transformations, weights)
            self.print_debug("will breed:")
            child = self._breed(trans1, trans2)
            new_seq = child(base_seq)
            if not isinstance(new_seq, CTSequence):
                new_seq = CTSequence(new_seq)
            self.print_debug("new_seq", str(result), str(new_seq))
            keep = self._fitness_func(result + new_seq)
            if keep:
                self.print_debug("OK, keeping")
                result = result + new_seq
                #update fitness of both parents
                i1 = self.transformations.index((trans1,w1))
                self.transformations[i1] = (trans1, w1+1)
                i2 = self.transformations.index((trans2,w2))
                self.transformations[i2] = (trans2, w2+1)
                #child inherits avg fitness of two parents
                new_weighting = int((w1 + w2)/2)
                self.transformations.append((child, new_weighting))
                base_seq = new_seq
                i = i+1
                #at the end of each round, possible random mutation in the gene pool...
                randy = random.random()
                if randy >= self.mutation_threshold:
                    # add random parents
                    (trans1,w1) = random.choice(self.transformations)
                    (trans2,w2) = random.choice(self.transformations)
                    if trans1 != trans2:
                        child = self._breed(trans1, trans2)
                    else:
                        child = self._breed(trans1)
                    self.print_debug("added new mutation to breeding pool:", child)
                    new_weighting = int((w1 + w2)/2)
                    self.transformations.append((child, new_weighting))
            else:
                score_down = 0.5
                #parents do not make a good breeding pair, score them down
                i1 = self.transformations.index((trans1,w1))
                if w1-score_down > 0:
                    self.transformations[i1] = (trans1, w1-score_down)
                else:
                    #the parent has partaken in too many bad offspring, so is extinct
                    del self.transformations[i1] #farewell noble beast
                i2 = self.transformations.index((trans2,w2))
                if w2-score_down > 0: 
                    self.transformations[i2] = (trans2, w2-score_down)
                else:
                    del self.transformations[i2] #farewell noble beast
        return (result, self.transformations)