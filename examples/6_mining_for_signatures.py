"""
Idea is a parse a piece of music in to the graph structure from eg 10

Then mine it for 4-5 note melodic signatures
     - intervals only, (ignore time for now)
     - allow extra notes (fuzzy)
     - allow intervals to change by one or two notes
     
Find most common out of the whole corpus

Then maybe, can the same be done with chords?
"""

from collections import namedtuple, OrderedDict
import itertools
import pprint

from functools import reduce

from mido import MidiFile

from resources import NOTE_MIN, NOTE_MAX


def parse_horizontal_edges(graph, track, trackid=0):
    """
    Parse a series of horizontal (monophonic) MIDI events
    into a directed graph structure.
    
    They are stored thus:
    
    {
        id1: [(id2, pitch_delta, time_delta)...],
        id2: [(id3, pitch_delta, time_delta)...]
        etc...
    }
    
    nb, in order to enable easy searching, the format 
    of the event ids is {trackid}-{pitch}-{time_ms}
    
    This provides the graph with horizontal motions.
    """
    note_off_events = filter(
        lambda x: x.type == "note_off", 
        filter(lambda x: x.is_meta == False, track))
    cumulative_time = 0
    previous_evt = None
    for evt in note_off_events:
        if previous_evt is None:
            previous_evt = evt
            continue
        previous_note_id = "{}-{}-{}".format(trackid, cumulative_time, previous_evt.note)
        cumulative_time = cumulative_time + evt.time
        edge = (
            "{}-{}-{}".format(trackid, cumulative_time, evt.note,),
            evt.note - previous_evt.note,
            previous_evt.time
        )
        try:
            graph[previous_note_id].append(edge)
        except KeyError:
            graph[previous_note_id] = [edge]
        previous_evt = evt
        
        
class Vertex(object):
    @classmethod
    def treeFromGraph(cls, graph):
        results = {}
        for key in graph.keys():
            v = Vertex(key)
            results[key] = v
        for key in graph.keys():
            node = results[key]
            neighbours = graph[key]
            for (name, pitch_delta, time_delta) in neighbours:
                try:
                    neighbour = results[name]
                except KeyError:
                    results[name] = Vertex(name)
                node.addNeighbour((pitch_delta, time_delta), results[name])
        return [v for k,v in results.items()]
                
    def __init__(self, name):
        self.name = name
        self.neighbours = []
        
    def __repr__(self):
        return "Vertex({})".format(self.name)
        
    def addNeighbour(self, vector, neighbour):
        self.neighbours.append((vector, neighbour))
        
mid = MidiFile('JSBach375Chorales\\chor001.mid')
connection_graph = OrderedDict({})
for i, track in enumerate(mid.tracks):
    parse_horizontal_edges(connection_graph, track, i)
    
tree = Vertex.treeFromGraph(connection_graph)

import collections
head = tree[0]
snips = collections.Counter()
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