def constraint_in_set(_set = range(0,128)):
    def f(seq, context):
        return seq.to_pitch_set().issubset(_set)
    return f
    
def constraint_no_repeated_adjacent_notes():
    def f(seq, context):
        return seq[0].pitch != context["previous"][-1].pitch
    return f
    
def constraint_limit_shared_pitches(max_shared=1):
    def f(seq, context):
        intersection = set(seq.pitches).intersection(set(context["previous"].pitches))
        return len(intersection) <= max_shared
    return f
    
def constraint_enforce_shared_pitches(min_shared=1):
    def f(seq, context):
        intersection = set(seq.pitches).intersection(set(context["previous"].pitches))
        return len(intersection) >= min_shared
    return f
    
def constraint_no_leaps_more_than(max_int):
    def f(context):
        event, seq, tick = context
        previous_pitch = seq[-1].pitch
        delta =  event.pitch - previous_pitch
        return abs(delta) <= max_int
    return f
    
def constraint_note_is(tick=0,pitch=0):
    def f(context):
        event, seq, _tick = context
        if _tick != tick:
            return True
        return event.pitch == pitch
    return f
    
def constraint_voice2_is_lower_than(voice1):
    def f(context):
        event, seq, tick = context
        #print(tick, voice1[tick], note, voice1[tick] >= note)
        return voice1[tick].pitch >= event.pitch
    return f