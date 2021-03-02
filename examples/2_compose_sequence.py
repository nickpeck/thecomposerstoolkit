import fluidsynth

from composerstoolkit.core import (CTEvent, 
    CTSequence, CTGenerator, CTTransformer, Container, chain)
from composerstoolkit.composers.solvers import (
    random_walk, random_walk_backtracking,
    random_walk_backtracking_w_heuristics)
from composerstoolkit.composers.evolutionary import Evolutionary, Extinction
from composerstoolkit.builder.transformers import transpose
from composerstoolkit.builder.generators import cantus, steady_pulse
from composerstoolkit.composers.constraints import constraint_in_set, constraint_no_leaps_more_than
from composerstoolkit.composers.heuristics import (
    heuristic_trend_upwards, heuristic_sine_shape)
from composerstoolkit.resources.scales import C_major
from composerstoolkit.builder.transformers import map_to_pulses

# intialise our synth
synth = fluidsynth.Synth()
synth.start()
sfid = synth.sfload("Nice-Steinway-v3.8.sf2")
synth.program_select(0, sfid, 0, 0)

# generate a random sequence that obeys the following constraints
sequence = random_walk_backtracking(
    60,
    10,
    [constraint_in_set(C_major), constraint_no_leaps_more_than(3)]
)

pulse_pattern = steady_pulse(0.2, 10)
sequence = sequence |chain| map_to_pulses(pulse_pattern)

print(sequence)

container = Container(bpm=160)
container.add_sequence(0, sequence)
container.playback(synth)