import fluidsynth
import time
import os
from dotenv import load_dotenv

import note

# .envファイルの内容を読み込む
load_dotenv()
SF2_PATH = os.environ.get("SF2_PATH")

if SF2_PATH is None:
    raise ValueError("SF2_PATHが読み込めません。.envファイルが存在するか確認してください。")

# FluidSynthの初期化とSoundfontのロード
fs = fluidsynth.Synth()
fs.start()

sfid = fs.sfload(SF2_PATH)
fs.program_select(0, sfid, 0, 0)

# 和音のMIDIノート番号を取得して、和音を鳴らす
notes = note.major_chord(note.note_to_midi("C", 4))
for n in notes:
    fs.noteon(0, n, 120)

time.sleep(3)

for n in notes:
    fs.noteoff(0, n)

fs.delete()
