import fluidsynth
import time
import os
from dotenv import load_dotenv

# .envファイルの内容を読み込む
load_dotenv()
SF2_PATH = os.environ.get("SF2_PATH")

if SF2_PATH is None:
    raise ValueError("SF2_PATHが読み込めません。.envファイルが存在するか確認してください。")

fs = fluidsynth.Synth()
fs.start()

sfid = fs.sfload(SF2_PATH)
fs.program_select(0, sfid, 0, 0)

fs.noteon(0, 60, 120)
fs.noteon(0, 64, 120)
fs.noteon(0, 67, 120)

time.sleep(3)

fs.noteoff(0, 60)