"""
In this example we try parsing a set of Bach Chorales into a directed graph format, which is
optimised for quick seachability. The primary goal is, given another graph to be able to quickly
determine if a transposition of that graph exists thing the case base, and then to 
return the surrounding context, so as to aid an inference engine.

However, there may be other data that can be mined from the case base.
"""

from collections import namedtuple, OrderedDict
import itertools
import pprint

from functools import reduce

from mido import MidiFile

from composerstoolkit import (NOTE_MIN, NOTE_MAX, Vertex,
find_matching_nodes, parse_to_connection_graph)

# open a chorole and parse into a graph structure
connection_graph = parse_to_connection_graph('JSBach375Chorales\\chor001.mid')

# this is a sub-graph that we'll search for:
# bar 14 sop jumping to alto in '1. Aus meines Herzens Grunde'
search_for = OrderedDict({
    "a": [("b", 4, 240)],
    "b": [("c", 3, 120)],
    "c": [("d", -2, 240)],
    "d": [("e", -6, 0)], # tritone leading to sop
    "e": []
})

matches = find_matching_nodes(
    Vertex.treeFromGraph(search_for), 
    Vertex.treeFromGraph(connection_graph))
    
print("MATCHES, EG1", pprint.pformat(matches, indent=4))


# same chorale, Chord V on start of bar 4
search_for = OrderedDict({
    "a": [("b", -3, 0)],
    "b": [("c", -4, 0)],
    "c": [("d", -12, 0)],
    "d": []
})

matches = find_matching_nodes(
    Vertex.treeFromGraph(search_for), 
    Vertex.treeFromGraph(connection_graph))
    
print("MATCHES, EG2", pprint.pformat(matches, indent=4))

