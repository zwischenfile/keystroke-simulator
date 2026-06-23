import sys
import datetime
import time
import ctypes
from pathlib import Path

import pydirectinput
import pyperclip

from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QCheckBox, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame,
    QMessageBox, QStatusBar
)

# ===== 설정 =====
TYPING_DELAY = 5
TYPING_INTERVAL = 0.05
LOG_FILE = Path(__file__).resolve().parent / "Log.txt"
FIXED_USER = "administrator"
WIN_WIDTH = 460
WIN_HEIGHT = 400
MARGIN_X = 10
MARGIN_Y = 50

SHIFT_MAP = {
    '!': '1', '@': '2', '#': '3', '$': '4', '%': '5',
    '^': '6', '&': '7', '*': '8', '(': '9', ')': '0',
    '_': '-', '+': '=',
    '{': '[', '}': ']', '|': '\\',
    ':': ';', '"': "'",
    '<': ',', '>': '.', '?': '/',
    '~': '`',
}


def is_running_as_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

# ===== 모던 다크 스타일시트 =====
STYLE_SHEET = """
QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: "Segoe UI", "Malgun Gothic", sans-serif;
    font-size: 10pt;
}
QLabel#titleLabel {
    font-size: 14pt;
    font-weight: bold;
    color: #89b4fa;
}
QLabel#fieldLabel {
    color: #a6adc8;
    font-size: 9pt;
}
QLineEdit {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 8px 10px;
    color: #cdd6f4;
    selection-background-color: #89b4fa;
}
QLineEdit:focus {
    border: 1px solid #89b4fa;
}
QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: none;
    border-radius: 6px;
    padding: 8px 14px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #45475a;
}
QPushButton:pressed {
    background-color: #585b70;
}
QPushButton#accentButton {
    background-color: #89b4fa;
    color: #1e1e2e;
    font-weight: bold;
}
QPushButton#accentButton:hover {
    background-color: #74a0e8;
}
QPushButton#accentButton:pressed {
    background-color: #5e8ad6;
}
QPushButton#dangerButton {
    background-color: #f38ba8;
    color: #1e1e2e;
    font-weight: bold;
}
QPushButton#dangerButton:hover {
    background-color: #e07a96;
}
QPushButton#dangerButton:pressed {
    background-color: #c96b85;
}
QCheckBox {
    color: #a6adc8;
    spacing: 6px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #45475a;
    background-color: #313244;
}
QCheckBox::indicator:checked {
    background-color: #89b4fa;
    border: 1px solid #89b4fa;
}
QFrame#separator {
    background-color: #45475a;
    max-height: 1px;
    min-height: 1px;
}
QStatusBar {
    background-color: #181825;
    color: #89b4fa;
    border-top: 1px solid #313244;
}
"""


class TypingWorker(QThread):
    """별도 스레드에서 카운트다운 + 타이핑 실행 (UI 블로킹 방지)"""
    status = Signal(str)
    finished_ok = Signal(str)
    finished_err = Signal(str)

    def __init__(self, text: str, label: str):
        super().__init__()
        self.text = text
        self.label = label

    def run(self):
        try:
            for remain in range(TYPING_DELAY, 0, -1):
                self.status.emit(
                    f"[{self.label}] {remain}초 후 타이핑... 입력창에 포커스 두세요."
                )
                time.sleep(1)

            for ch in self.text:
                self._press_char(ch)
                time.sleep(TYPING_INTERVAL)

            self.finished_ok.emit(f"[{self.label}] 타이핑 완료")
        except Exception as e:
            self.finished_err.emit(f"[{self.label}] 타이핑 실패: {e}")

    @staticmethod
    def _press_char(ch: str):
        if ch == ' ':
            pydirectinput.press('space'); return
        if ch == '\t':
            pydirectinput.press('tab'); return
        if ch == '\n':
            pydirectinput.press('enter'); return

        if ch.isupper():
            pydirectinput.keyDown('shift')
            try: pydirectinput.press(ch.lower())
            finally: pydirectinput.keyUp('shift')
        elif ch in SHIFT_MAP:
            pydirectinput.keyDown('shift')
            try: pydirectinput.press(SHIFT_MAP[ch])
            finally: pydirectinput.keyUp('shift')
        else:
            pydirectinput.press(ch)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.worker: TypingWorker | None = None

        self.setWindowTitle("ID/PW 도우미")
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self._build_ui()
        self._move_to_bottom_right()

    # ---------- UI 구성 ----------
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 0)
        root.setSpacing(10)

        # 타이틀
        title = QLabel("ID / PW 도우미")
        title.setObjectName("titleLabel")
        root.addWidget(title)

        # 입력 영역
        lbl_id = QLabel("ID (호스트네임)")
        lbl_id.setObjectName("fieldLabel")
        self.entry_id = QLineEdit()
        self.entry_id.setPlaceholderText("예: MYHOST")

        lbl_pw = QLabel("PW")
        lbl_pw.setObjectName("fieldLabel")
        self.entry_pw = QLineEdit()
        self.entry_pw.setPlaceholderText("비밀번호")
        # self.entry_pw.setEchoMode(QLineEdit.Password)  # 마스킹 원하면 주석 해제

        root.addWidget(lbl_id)
        root.addWidget(self.entry_id)
        root.addWidget(lbl_pw)
        root.addWidget(self.entry_pw)

        # 버튼 그리드 (복사/타이핑)
        btn_grid = QGridLayout()
        btn_grid.setHorizontalSpacing(8)
        btn_grid.setVerticalSpacing(6)

        btn_copy_id = QPushButton("ID 복사")
        btn_copy_pw = QPushButton("PW 복사")
        btn_type_id = QPushButton("ID 타이핑")
        btn_type_pw = QPushButton("PW 타이핑")

        btn_type_id.setObjectName("accentButton")
        btn_type_pw.setObjectName("accentButton")

        btn_copy_id.clicked.connect(self.on_copy_id)
        btn_copy_pw.clicked.connect(self.on_copy_pw)
        btn_type_id.clicked.connect(self.on_type_id)
        btn_type_pw.clicked.connect(self.on_type_pw)

        btn_grid.addWidget(btn_copy_id, 0, 0)
        btn_grid.addWidget(btn_copy_pw, 0, 1)
        btn_grid.addWidget(btn_type_id, 1, 0)
        btn_grid.addWidget(btn_type_pw, 1, 1)
        root.addLayout(btn_grid)

        # ID/PW 삭제 버튼 (강조 빨강)
        btn_clear = QPushButton("ID/PW 삭제")
        btn_clear.setObjectName("dangerButton")
        btn_clear.clicked.connect(self.on_clear)
        root.addWidget(btn_clear)

        # 옵션
        opt_row = QHBoxLayout()
        self.chk_topmost = QCheckBox("항상 위에 표시")
        self.chk_topmost.toggled.connect(self.on_toggle_topmost)
        opt_row.addWidget(self.chk_topmost)
        opt_row.addStretch()
        root.addLayout(opt_row)

        # 분리선
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.HLine)
        root.addWidget(sep)

        # 상태바
        self.status = QStatusBar()
        self.status.showMessage("대기 중")
        root.addWidget(self.status)

    def _move_to_bottom_right(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        x = screen.right() - WIN_WIDTH - MARGIN_X
        y = screen.bottom() - WIN_HEIGHT - MARGIN_Y
        self.move(x, y)

    # ---------- 헬퍼 ----------
    def get_values(self):
        return self.entry_id.text().strip(), self.entry_pw.text()

    def write_log_if_needed(self, host_id: str, pw: str):
        if not host_id or not pw:
            return
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{now} | ID={host_id} | PW={pw}\n"
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception as e:
            print(f"로그 기록 실패: {e}")

    def set_status(self, msg: str):
        self.status.showMessage(msg)

    def warn(self, msg: str):
        QMessageBox.warning(self, "경고", msg)

    # ---------- 동작 ----------
    def on_copy_id(self):
        host_id, pw = self.get_values()
        if not host_id:
            self.warn("ID(호스트네임)를 입력하세요."); return
        text = f"{host_id}\\{FIXED_USER}"
        pyperclip.copy(text)
        self.write_log_if_needed(host_id, pw)
        self.set_status(f"복사됨: {text}")

    def on_copy_pw(self):
        host_id, pw = self.get_values()
        if not pw:
            self.warn("PW를 입력하세요."); return
        pyperclip.copy(pw)
        self.write_log_if_needed(host_id, pw)
        self.set_status("PW 클립보드에 복사됨")

    def on_type_id(self):
        host_id, pw = self.get_values()
        if not host_id:
            self.warn("ID(호스트네임)를 입력하세요."); return
        self.write_log_if_needed(host_id, pw)
        text = f"{host_id}\\{FIXED_USER}"
        self._start_typing(text, "ID")

    def on_type_pw(self):
        host_id, pw = self.get_values()
        if not pw:
            self.warn("PW를 입력하세요."); return
        self.write_log_if_needed(host_id, pw)
        self._start_typing(pw, "PW")

    def on_clear(self):
        self.entry_id.clear()
        self.entry_pw.clear()
        self.entry_id.setFocus()
        self.set_status("ID/PW 삭제됨")

    def _start_typing(self, text: str, label: str):
        if self.worker and self.worker.isRunning():
            self.set_status("이전 작업 진행 중입니다...")
            return
        self.worker = TypingWorker(text, label)
        self.worker.status.connect(self.set_status)
        self.worker.finished_ok.connect(self.set_status)
        self.worker.finished_err.connect(self.set_status)
        self.worker.start()

    def on_toggle_topmost(self, checked: bool):
        # WindowStaysOnTopHint 토글하려면 윈도우 플래그 변경 후 다시 show 필요
        flags = self.windowFlags()
        if checked:
            flags |= Qt.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.show()
        self.set_status(f"항상 위: {'ON' if checked else 'OFF'}")


def main():
    app = QApplication(sys.argv)
    if not is_running_as_admin():
        QMessageBox.warning(
            None,
            "관리자 권한 필요",
            "이 프로그램은 관리자 권한으로 실행해야 합니다.\n프로그램을 종료합니다.",
        )
        sys.exit(1)

    app.setStyleSheet(STYLE_SHEET)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
