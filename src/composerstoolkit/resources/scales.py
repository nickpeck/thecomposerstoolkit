from . import NOTE_MIN, NOTE_MAX

MAJ_SCALE_PITCH_CLASSES = {0,2,4,5,7,9,11}
MEL_MINOR_SCALE_PITCH_CLASSES = {0,2,3,5,7,9,11}
HAR_MINOR_SCALE_PITCH_CLASSES = {0,2,3,5,7,8,11}
CHROMATIC_SCALE_PITCH_CLASSES = {*[range(0,11)]}

C_major = [0] + sorted(filter(lambda x: (x % 12) in \
    MAJ_SCALE_PITCH_CLASSES, range(1, NOTE_MAX)))
Db_major = set(map(lambda x: x+1, C_major))
D_major = set(map(lambda x: x+2, C_major))
Eb_major = set(map(lambda x: x+3, C_major))
E_major = set(map(lambda x: x+4, C_major))
F_major = set(map(lambda x: x+5, C_major))
Gb_major = set(map(lambda x: x+6, C_major))
G_major = set(map(lambda x: x+7, C_major))
Ab_major = set(map(lambda x: x+8, C_major))
A_major = set(map(lambda x: x+9, C_major))
Bb_major = set(map(lambda x: x+10, C_major))
B_major = set(map(lambda x: x+11, C_major))

C_mel_minor = [0] + sorted(filter(lambda x: (x % 12) in \
    MEL_MINOR_SCALE_PITCH_CLASSES, range(1, NOTE_MAX)))
Db_mel_minor = map(lambda x: x+1, C_mel_minor)
D_mel_minor = map(lambda x: x+2, C_mel_minor)
Eb_mel_minor = map(lambda x: x+3, C_mel_minor)
E_mel_minor = map(lambda x: x+4, C_mel_minor)
F_mel_minor = map(lambda x: x+5, C_mel_minor)
Gb_mel_minor = map(lambda x: x+6, C_mel_minor)
G_mel_minor = map(lambda x: x+7, C_mel_minor)
Ab_mel_minor = map(lambda x: x+8, C_mel_minor)
A_mel_minor = map(lambda x: x+9, C_mel_minor)
Bb_mel_minor = map(lambda x: x+10, C_mel_minor)
B_mel_minor = map(lambda x: x+11, C_mel_minor)

C_har_minor = [0] + sorted(filter(lambda x: (x % 12) in \
    HAR_MINOR_SCALE_PITCH_CLASSES , range(1, NOTE_MAX)))
Db_har_minor = map(lambda x: x+1, C_mel_minor)
D_har_minor = map(lambda x: x+2, C_major)
Eb_har_minor = map(lambda x: x+3, C_major)
E_har_minor = map(lambda x: x+4, C_major)
F_har_minor = map(lambda x: x+5, C_major)
Gb_har_minor = map(lambda x: x+6, C_major)
G_har_minor = map(lambda x: x+7, C_major)
Ab_har_minor = map(lambda x: x+8, C_major)
A_har_minor = map(lambda x: x+9, C_major)
Bb_har_minor = map(lambda x: x+10, C_major)
B_har_minor = map(lambda x: x+11, C_major)