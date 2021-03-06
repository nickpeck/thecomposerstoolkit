import fluidsynth
from composerstoolkit import (chain, Container,
cantus, cantus_from_pulses, permutate, map_to_pulses)

# intialise our synth
synth = fluidsynth.Synth()
synth.start()
sfid = synth.sfload("Nice-Steinway-v3.8.sf2")
synth.program_select(0, sfid, 0, 0)

# generate a permutated sequence of pitch events
# mapped to a steady pulse

pitch_classes = {60,66,67}
pitch_permutations = permutate(pitch_classes)
melody = cantus([i for sub in pitch_permutations for i in sub])

durations = [0.25,0.5,0.5,1.0]
pulse_permutations = permutate(durations)
pulse_pattern = cantus_from_pulses([i for sub in pulse_permutations for i in sub])

sequence = melody |chain| map_to_pulses(pulse_pattern)

container = Container(bpm=160)
container.add_sequence(0, sequence)
container.playback(synth)
container.save_as_midi_file("1_simple_melodic_generator.mid")