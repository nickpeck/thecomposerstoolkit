import fluidsynth
from composerstoolkit import (chain, Container, aggregate_into_chords, CTEvent,
cantus, cantus_from_pulses, permutate, map_to_pulses, loop, CTSequence)

from functools import reduce

# intialise our synth
synth = fluidsynth.Synth()
synth.start()
sfid = synth.sfload("Nice-Steinway-v3.8.sf2")
synth.program_select(0, sfid, 0, 0)

N_VOICES = 5

# the source is Messiaen's mode 4 arranged in thirds
mode_4_pitch_classes = [0,2,6,8,1,5,7,11]
pitches = cantus([60 + p for p  in mode_4_pitch_classes]) |chain| \
    loop(len(mode_4_pitch_classes) * N_VOICES)

# now, aggregate these into 4 note chords
pitch_sequence = pitches.chain(aggregate_into_chords(N_VOICES))

# lets have an interesting rhythm to map these to (see ex 1)
durations = [0.25,0.5,0.5,1.0]
pulse_permutations = permutate(durations)
pulse_pattern = cantus_from_pulses([i for sub in pulse_permutations for i in sub]) \
    |chain| loop(len(mode_4_pitch_classes) * N_VOICES)

sequence = pitch_sequence |chain| map_to_pulses(pulse_pattern)

# play them back
container = Container(bpm=160)
container.add_sequence(0, sequence)
container.playback(synth)
container.save_as_midi_file("4_chord_generator.mid")
