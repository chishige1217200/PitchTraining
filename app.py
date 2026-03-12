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
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt

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
# ピアノロール
# -----------------------------
class PianoRoll(QWidget):

    def __init__(self):
        super().__init__()

        self.notes = []

        self.white_keys = [0,2,4,5,7,9,11]

        self.setMinimumHeight(120)

    def set_notes(self, notes):
        self.notes = [n % 12 for n in notes]
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        w = self.width()
        h = self.height()

        white_w = w / 7

        # 枠線設定
        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        # ---- 白鍵 ----
        for i, note in enumerate(self.white_keys):

            x = i * white_w

            if note in self.notes:
                painter.setBrush(QColor(255,120,120))
            else:
                painter.setBrush(QColor(255,255,255))

            painter.drawRect(x,0,white_w,h)

        # ---- 黒鍵 ----
        black_positions = {
            1:0.7,
            3:1.7,
            6:3.7,
            8:4.7,
            10:5.7
        }

        bw = white_w * 0.6
        bh = h * 0.6

        for note,pos in black_positions.items():

            x = pos * white_w

            if note in self.notes:
                painter.setBrush(QColor(200,0,0))
            else:
                painter.setBrush(QColor(0,0,0))

            painter.drawRect(x,0,bw,bh)

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

        self.piano = PianoRoll()
        layout.addWidget(self.piano)

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

        if self.last_notes:
            self.piano.set_notes(self.last_notes)


# -----------------------------
# 起動
# -----------------------------
if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = EarTrainingApp()
    window.resize(300,250)
    window.show()

    sys.exit(app.exec())