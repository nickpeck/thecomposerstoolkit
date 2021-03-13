import fluidsynth

from composerstoolkit import (Container, chain, random_walk_backtracking,
steady_pulse, constraint_in_set, constraint_no_leaps_more_than, map_to_pulses, scales)

# intialise our synth
synth = fluidsynth.Synth()
synth.start()
sfid = synth.sfload("Nice-Steinway-v3.8.sf2")
synth.program_select(0, sfid, 0, 0)

# generate a random sequence that obeys the following constraints
sequence = random_walk_backtracking(
    60,
    10,
    [constraint_in_set(scales.C_major), constraint_no_leaps_more_than(3)]
)

pulse_pattern = steady_pulse(0.2, 10)
sequence = sequence |chain| map_to_pulses(pulse_pattern)

print(sequence)

container = Container(bpm=160)
container.add_sequence(0, sequence)
container.playback(synth)