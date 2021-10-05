from collections import OrderedDict
from mido import MidiFile

def _parse_horizontal_edges(graph, track, trackid=0):
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
        
def _parse_vertical_edges(graph):
    """
        Parse vertical graph connections between notes in different
        tracks that start on the same beat.
    """
    for ident in graph.keys():
        id1, time1, p1 = ident.split("-")
        matching_keys = [ k for k,v in graph.items() if '-' + time1 + '-' in k]
        matching_keys.remove(ident)
        # these are now basically all the notes that start at the same time (ie chord)
        for candidate_link in matching_keys:
            id2, time2, p2 = candidate_link.split("-")
            if int(id2) == int(id1)-1: #lower voice
                edge = (
                    candidate_link,
                    int(p2)-int(p1),
                    0 # they are all at the same time, so this is 0
                )
                graph[ident].append(edge)
            elif int(id2)== int(id1)+1: #upper voice
                edge = (
                    candidate_link,
                    int(p2)-int(p1),
                    0 # they are all at the same time, so this is 0
                )
                graph[ident].append(edge)
                
# convenience method based on the above - TODO refactor into a connection_graph class
def parse_to_connection_graph(midifile_name):
    mid = MidiFile(midifile_name)
    connection_graph = OrderedDict({})
    for i, track in enumerate(mid.tracks):
        _parse_horizontal_edges(connection_graph, track, i)
    _parse_vertical_edges(connection_graph)
    return connection_graph

                
# TODO this should be deprecated - can lead to memoryerror
def all_routes(graph):
    """
    Given the connection graph, provide a list of all possible
    (maximal continuous) routes within that graph.
    
    For example, where the actual sequence of notes might be
    c->d->e->f, the possible routes within, assuming only forwards
    motion, is
    [[c,d,e,f]]
    """
    routes = []
    already_visited = []
    for node in graph.keys():
        if node in already_visited:
            continue
        already_visited.append(node)
        nodes_to_explore = [([],candidate) for candidate in graph[node]]
        while len(nodes_to_explore) > 0:
            route,candidate = nodes_to_explore.pop()
            nodeid,pitch,time = candidate #should be pitch_delta, time_delta
            already_visited.append(nodeid)
            route.append((pitch,time))
            try:
                new_candidates = [(route[:],c) for c in graph[nodeid]]
                nodes_to_explore = nodes_to_explore + new_candidates
            except KeyError:
                routes.append((node,route))
    return sorted(routes)
    
def find_matching_nodes(search_for, search_in, matches=[]):
    """
    Search Vertex tree 'search_in' for the first isomorphic occurance of the 
    Vertex tree search_for
    
    Return a list of [(x,y)...] for node in search_for (x) matched with 
    a pair (y) from search in, such as the two graphs preserve their linking
    vectors. From this, we might be able to determine the wider context,
    and therefore provide a suggestion as to how to compose out search_for,
    in the style of search_in.
    
    Return None, if a match cannot be made.
    If allow_partial is True, then in the event that a complete set of matches
    cannot be made, return only those nodes for which a twin can be found.
    
    matches - is s a list of matches to ignore (allowing the callee to 'mine'
    for alternatives).
    """
    matches = []
    for v1 in search_for:
        # at each root node in search_for, we start to compose a
        # temporary tree, to hold our solution
        temp_tree = None
        found_match = False
        if v1 in [x for (x,y) in matches]:
            # the node v2 has already been matched, so pass
            continue
        for v2 in search_in:
            if v2 in [y for (x,y) in matches]:
                # the node v2 has already been matched, so pass
                continue
            # so we have found a new, unexplored node. Start building a potential solution:
            solution = []
            # fan out the neighbours of both nodes:
            temp_tree = v2.neighbours
            to_match = v1.neighbours
            while len(to_match) > 0:
                vectors_to_match = [v for (v,n) in to_match]
                vectors_temp_tree = [v for (v,n) in temp_tree]
                # we ask; are all the vectors joining the current node of 'search_in'
                # to its neighbours, to be found at the reciprocal point search_in?
                if len(list(filter(lambda x: x in vectors_temp_tree, vectors_to_match))) != 0:
                    # Ok, they match so far. Add each of these neighbours to the expanding solution:
                    for a,b in to_match:
                        for x,y in temp_tree:
                            if a == x:
                                solution.append((b,y))
                            else:
                                temp_tree.remove((x,y))
                                
                    # now we drill down to the next layer of neighbour nodes on both sides:
                    _temp_tree = []
                    for (v,n) in temp_tree:
                        _temp_tree = _temp_tree  + n.neighbours
                    _to_match = []
                    for (v,n) in to_match:
                        _to_match = _to_match + n.neighbours
                    to_match = _to_match
                    temp_tree = _temp_tree
                            
                else:
                    # in this case trees do not match, will not explore this avenue further
                    break
                    
            # at the point that to_match is empty, we have found a complete, matching tree
            if to_match == []:
                found_match = True
                matches = matches + [(v1,v2)] + solution
                break
        if not found_match:
            # Did not find a match anywhere for v1 and its children
            return []
    # 'happy path' outcome, isomorphic match was located
    return matches