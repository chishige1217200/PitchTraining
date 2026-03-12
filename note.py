NOTE_MAP = {
    "C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4,
    "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11
}


def note_to_midi(note, octave):
    """音符とオクターブをMIDIノート番号に変換する"""
    return NOTE_MAP[note] + (octave + 1) * 12


def major_chord(root):
    """ルート音のMIDIノート番号を受け取り、メジャーコードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+4, root+7]


def minor_chord(root):
    """ルート音のMIDIノート番号を受け取り、マイナーコードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+3, root+7]


def diminished_chord(root):
    """ルート音のMIDIノート番号を受け取り、ディミニッシュコードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+3, root+6]


def augmented_chord(root):
    """ルート音のMIDIノート番号を受け取り、オーギュメントコードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+4, root+8]


# --- 7th系 ---
def dominant7_chord(root):
    """ルート音のMIDIノート番号を受け取り、ドミナント7コードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+4, root+7, root+10]


def major7_chord(root):
    """ルート音のMIDIノート番号を受け取り、メジャー7コードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+4, root+7, root+11]


def minor7_chord(root):
    """ルート音のMIDIノート番号を受け取り、マイナー7コードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+3, root+7, root+10]


def minor_major7_chord(root):
    """ルート音のMIDIノート番号を受け取り、マイナーMajor7コードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+3, root+7, root+11]


def half_diminished7_chord(root):
    """ルート音のMIDIノート番号を受け取り、ハーフディミニッシュ7コードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+3, root+6, root+10]


def diminished7_chord(root):
    """ルート音のMIDIノート番号を受け取り、ディミニッシュ7コードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+3, root+6, root+9]


# --- sus系 ---
def sus2_chord(root):
    """ルート音のMIDIノート番号を受け取り、sus2コードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+2, root+7]


def sus4_chord(root):
    """ルート音のMIDIノート番号を受け取り、sus4コードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+5, root+7]


# --- add系 ---
def add9_chord(root):
    """ルート音のMIDIノート番号を受け取り、add9コードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+4, root+7, root+14]


def minor_add9_chord(root):
    """ルート音のMIDIノート番号を受け取り、マイナーadd9コードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+3, root+7, root+14]


# --- 6系 ---
def sixth_chord(root):
    """ルート音のMIDIノート番号を受け取り、6コードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+4, root+7, root+9]


def minor_sixth_chord(root):
    """ルート音のMIDIノート番号を受け取り、マイナー6コードの構成音のMIDIノート番号をリストで返す"""
    return [root, root+3, root+7, root+9]
