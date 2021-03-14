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

# the source is Messiaen's mode 3 arranged in thirds
mode_4_pitch_classes = {0,3,6,8,11,14,16,19,22}
pitches = cantus([60 + p for p  in mode_4_pitch_classes]) |chain| \
    loop(len(mode_4_pitch_classes) * N_VOICES)

# now, aggregate these into 4 note chords
pitch_sequence = pitches.chain(aggregate_into_chords())

# play them back
container = Container(bpm=160)
container.add_sequence(0, pitch_sequence)
container.playback(synth)
