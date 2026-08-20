"""
AURA AI - Futuristic HUD Interface
Version: 0.40.0
"""

import sys
import psutil

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.brain.brain import Brain
from src.core.orchestrator import Orchestrator


CYAN = "#35dfff"
DARK = "#05080d"
PANEL = "#09121b"
TEXT = "#d9f9ff"
MUTED = "#6e9aa5"


class AuraHUD(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AURA AI")
        self.resize(1400, 850)
        self.setMinimumSize(1000, 650)

        self.brain = Brain()
        self.orchestrator = Orchestrator(self.brain)
        
        self.setup_ui()
        self.setup_timer()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def setup_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        # ================= HEADER =================

        header = QHBoxLayout()

        title = QLabel("A U R A")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setStyleSheet(f"color: {CYAN};")

        subtitle = QLabel("  ARTIFICIAL INTELLIGENCE SYSTEM")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setStyleSheet(f"color: {MUTED};")

        header.addWidget(title)
        header.addWidget(subtitle)
        header.addStretch()

        self.security = QLabel("● SECURITY: LOCKED")
        self.security.setStyleSheet(
            f"""
            color: {CYAN};
            font-weight: bold;
            padding: 8px 14px;
            border: 1px solid {CYAN};
            """
        )

        header.addWidget(self.security)

        root.addLayout(header)

        # ================= MAIN =================

        main = QHBoxLayout()
        main.setSpacing(14)

        # -------- LEFT PANEL --------

        left = self.panel()
        left_layout = QVBoxLayout(left)

        left_layout.addWidget(self.section_title("SYSTEM"))

        self.cpu_label = QLabel("CPU     -- %")
        self.ram_label = QLabel("RAM     -- %")
        self.process_label = QLabel("PROCESSES     --")

        for label in (
            self.cpu_label,
            self.ram_label,
            self.process_label,
        ):
            label.setStyleSheet(f"color: {TEXT};")
            left_layout.addWidget(label)

        left_layout.addSpacing(20)

        left_layout.addWidget(self.section_title("AURA CORE"))

        self.core_status = QLabel("● ONLINE")
        self.core_status.setAlignment(Qt.AlignCenter)
        self.core_status.setFont(QFont("Arial", 18, QFont.Bold))
        self.core_status.setStyleSheet(
            f"""
            color: {CYAN};
            border: 1px solid {CYAN};
            padding: 28px;
            """
        )

        left_layout.addWidget(self.core_status)
        left_layout.addStretch()

        main.addWidget(left, 1)

        # -------- CENTER PANEL --------

        center = self.panel()
        center_layout = QVBoxLayout(center)

        self.mode = QLabel("AURA CORE")
        self.mode.setAlignment(Qt.AlignCenter)
        self.mode.setFont(QFont("Arial", 22, QFont.Bold))
        self.mode.setStyleSheet(f"color: {CYAN};")

        center_layout.addWidget(self.mode)

        self.core = QLabel("◉")
        self.core.setAlignment(Qt.AlignCenter)
        self.core.setFont(QFont("Arial", 150, QFont.Bold))
        self.core.setStyleSheet(
            f"""
            color: {CYAN};
            padding: 30px;
            """
        )

        center_layout.addWidget(self.core)

        self.core_info = QLabel(
            "SYSTEM READY\n\n"
            "WAITING FOR COMMAND"
        )
        self.core_info.setAlignment(Qt.AlignCenter)
        self.core_info.setFont(QFont("Arial", 11))
        self.core_info.setStyleSheet(f"color: {MUTED};")

        center_layout.addWidget(self.core_info)

        center_layout.addStretch()

        main.addWidget(center, 2)

        # -------- RIGHT PANEL --------

        right = self.panel()
        right_layout = QVBoxLayout(right)

        right_layout.addWidget(self.section_title("STATUS"))

        self.status_brain = QLabel("BRAIN       READY")
        self.status_memory = QLabel("MEMORY      READY")
        self.status_voice = QLabel("VOICE       STANDBY")
        self.status_security = QLabel("SECURITY    LOCKED")

        for label in (
            self.status_brain,
            self.status_memory,
            self.status_voice,
            self.status_security,
        ):
            label.setStyleSheet(f"color: {TEXT};")
            right_layout.addWidget(label)

        right_layout.addSpacing(20)

        right_layout.addWidget(self.section_title("ACTIVITY"))

        self.activity = QLabel(
            "AURA initialized.\n"
            "Awaiting user command..."
        )
        self.activity.setWordWrap(True)
        self.activity.setStyleSheet(f"color: {MUTED};")

        right_layout.addWidget(self.activity)
        right_layout.addStretch()

        main.addWidget(right, 1)

        root.addLayout(main, 1)

        # ================= COMMAND BAR =================

        command_panel = QFrame()
        command_panel.setStyleSheet(
            f"""
            QFrame {{
                background: {PANEL};
                border: 1px solid {CYAN};
            }}
            """
        )

        command_layout = QHBoxLayout(command_panel)
        command_layout.setContentsMargins(12, 8, 12, 8)

        prompt = QLabel("AURA >")
        prompt.setFont(QFont("Arial", 12, QFont.Bold))
        prompt.setStyleSheet(f"color: {CYAN};")

        command_layout.addWidget(prompt)

        self.command = QLineEdit()
        self.command.setPlaceholderText(
            "Enter command for AURA..."
        )
        self.command.setFont(QFont("Arial", 12))
        self.command.setStyleSheet(
            f"""
            QLineEdit {{
                background: transparent;
                color: {TEXT};
                border: none;
                padding: 8px;
            }}
            """
        )

        self.command.returnPressed.connect(self.process_command)

        command_layout.addWidget(self.command)

        send = QPushButton("EXECUTE")
        send.setCursor(Qt.PointingHandCursor)
        send.clicked.connect(self.process_command)

        send.setStyleSheet(
            f"""
            QPushButton {{
                background: transparent;
                color: {CYAN};
                border: 1px solid {CYAN};
                padding: 8px 18px;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background: {CYAN};
                color: {DARK};
            }}
            """
        )

        command_layout.addWidget(send)

        root.addWidget(command_panel)

        # ================= GLOBAL STYLE =================

        self.setStyleSheet(
            f"""
            QMainWindow {{
                background: {DARK};
            }}

            QWidget {{
                background: {DARK};
                color: {TEXT};
            }}

            QFrame {{
                background: {PANEL};
                border: 1px solid #173441;
            }}
            """
        )

        self.command.setFocus()

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def panel(self):

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)

        return frame

    def section_title(self, text):

        label = QLabel(text)
        label.setFont(QFont("Arial", 10, QFont.Bold))
        label.setStyleSheet(
            f"""
            color: {CYAN};
            padding-bottom: 8px;
            """
        )

        return label

    # ---------------------------------------------------------
    # Commands
    # ---------------------------------------------------------

    def process_command(self):

        command = self.command.text().strip()

        if not command:
            return

        self.command.clear()

        self.mode.setText("THINKING")
        self.core_info.setText(
            f'PROCESSING...\n\n"{command}"'
        )

        self.activity.setText(
            f"USER COMMAND:\n{command}\n\n"
            "AURA processing request..."
        )

        self.status_brain.setText("BRAIN       THINKING")

        try:
            response = self.orchestrator.handle(command)

            self.mode.setText("AURA CORE")

            self.core_info.setText(
                "SYSTEM READY\n\n"
                "RESPONSE GENERATED"
            )

            self.activity.setText(
                f"USER COMMAND:\n{command}\n\n"
                f"AURA:\n{response}"
            )

            self.status_brain.setText("BRAIN       READY")

        except Exception as exc:

            self.mode.setText("ERROR")

            self.core_info.setText(
                "PROCESSING ERROR"
            )

            self.activity.setText(
                f"COMMAND:\n{command}\n\n"
                f"ERROR:\n{exc}"
            )

            self.status_brain.setText("BRAIN       ERROR")

    # ---------------------------------------------------------
    # System Monitor
    # ---------------------------------------------------------

    def setup_timer(self):

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system)
        self.timer.start(1500)

        self.update_system()

    def update_system(self):

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        processes = len(psutil.pids())

        self.cpu_label.setText(
            f"CPU          {cpu:.1f}%"
        )

        self.ram_label.setText(
            f"RAM          {ram:.1f}%"
        )

        self.process_label.setText(
            f"PROCESSES    {processes}"
        )


def launch():

    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)

    window = AuraHUD()
    window.show()

    return app.exec()


if __name__ == "__main__":
    launch()
