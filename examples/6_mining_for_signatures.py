"""
Idea is a parse a piece of music in to the graph structure from eg 10

Then mine it for 4-5 note melodic signatures
     - intervals only, (ignore time for now)
     - allow extra notes (fuzzy)
     - allow intervals to change by one or two notes
     
Find most common out of the whole corpus

Then maybe, can the same be done with chords?
"""

from collections import Counter, namedtuple, OrderedDict
import itertools
import pprint

from functools import reduce

from mido import MidiFile

from composerstoolkit import (NOTE_MIN, NOTE_MAX, Vertex,
parse_to_connection_graph)

# open a chorole and parse into a graph structure
connection_graph = parse_to_connection_graph('JSBach375Chorales\\chor001.mid')
  
    
tree = Vertex.treeFromGraph(connection_graph)

import collections
head = tree[0]
snips = Counter()
l = []
while head.neighbours != []:
    vector, head = head.neighbours[0]
    l.append(vector[0])
    if len(l) > 5:
        snips.update(l[-4:])
    
print(l)
print(snips)
exit()
import math

def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)
    
print(Counter(snips))
    
for s1 in snips:
    for s2 in snips:
        r = counter_cosine_similarity(s1,s2)
        print(s1,s2,r)