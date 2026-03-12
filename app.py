import sys
import random
import time
import threading

import fluidsynth
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
)

import os
from dotenv import load_dotenv

# .envファイルの内容を読み込む
load_dotenv()
SF2_PATH = os.environ.get("SF2_PATH")

if SF2_PATH is None:
    raise ValueError("SF2_PATHが読み込めません。.envファイルが存在するか確認してください。")


NOTE_NAMES = [
    "C","C#","D","D#","E","F",
    "F#","G","G#","A","A#","B"
]

NOTE_DISPLAY_NAMES = [
    "ド","ド#","レ","レ#","ミ","ファ",
    "ファ#","ソ","ソ#","ラ","ラ#","シ"
]

BASE_NOTE = 60


# -----------------------------
# 和音
# -----------------------------
def major_chord(root):
    return [root, root+4, root+7]

def minor_chord(root):
    return [root, root+3, root+7]

def dim_chord(root):
    return [root, root+3, root+6]

def aug_chord(root):
    return [root, root+4, root+8]


CHORD_TYPES = {
    "Major": major_chord,
    "Minor": minor_chord,
    "Dim": dim_chord,
    "Aug": aug_chord,
}


# -----------------------------
# FluidSynth
# -----------------------------
def create_synth():
    fs = fluidsynth.Synth()
    fs.start()

    sfid = fs.sfload(SF2_PATH)
    fs.program_select(0, sfid, 0, 0)

    return fs


# -----------------------------
# メインアプリ
# -----------------------------
class EarTrainingApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ear Training")

        self.fs = create_synth()

        self.correct_note = None
        self.correct_chord = None
        self.last_notes = None

        layout = QVBoxLayout()

        self.mode_select = QComboBox()
        self.mode_select.addItems(["Single Note", "Chord"])
        layout.addWidget(self.mode_select)

        self.label = QLabel("Press Play")
        layout.addWidget(self.label)

        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.play_question)
        layout.addWidget(self.play_btn)

        self.play_again_btn = QPushButton("Play Again")
        self.play_again_btn.clicked.connect(self.play_again)
        layout.addWidget(self.play_again_btn)

        self.answer = QComboBox()
        self.answer.addItems(NOTE_DISPLAY_NAMES)
        layout.addWidget(self.answer)

        self.check_btn = QPushButton("Check")
        self.check_btn.clicked.connect(self.check_answer)
        layout.addWidget(self.check_btn)

        self.result = QLabel("")
        layout.addWidget(self.result)

        self.setLayout(layout)

    # -------------------------
    # 音再生
    # -------------------------
    def play_notes(self, notes):

        def run():
            for n in notes:
                self.fs.noteon(0, n, 100)

            time.sleep(1.5)

            for n in notes:
                self.fs.noteoff(0, n)

        threading.Thread(target=run).start()

    # -------------------------
    # 問題生成
    # -------------------------
    def play_question(self):

        mode = self.mode_select.currentText()

        if mode == "Single Note":

            note = BASE_NOTE + random.randint(0, 11)
            self.correct_note = note % 12
            notes = [note]

        else:

            root = BASE_NOTE + random.randint(0, 11)
            chord_name, func = random.choice(list(CHORD_TYPES.items()))

            notes = func(root)

            self.correct_note = root % 12
            self.correct_chord = chord_name

        self.last_notes = notes

        self.play_notes(notes)

        self.result.setText("")

    # -------------------------
    # 再生し直し
    # -------------------------
    def play_again(self):

        if self.last_notes:
            self.play_notes(self.last_notes)

    # -------------------------
    # 回答チェック
    # -------------------------
    def check_answer(self):

        ans = self.answer.currentText()
        ans_index = NOTE_DISPLAY_NAMES.index(ans)

        if ans_index == self.correct_note:
            self.result.setText("Correct!")
        else:
            correct = NOTE_NAMES[self.correct_note]
            self.result.setText(f"Wrong (Answer: {correct})")


# -----------------------------
# 起動
# -----------------------------
if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = EarTrainingApp()
    window.resize(300,250)
    window.show()

    sys.exit(app.exec())