"""
AURA AI - JARVIS STYLE COMMAND CENTER
Version: 0.82.0

UI-only upgrade.
Existing backend integrations are preserved:
    Brain
    Orchestrator
    VoiceManager
    psutil

No new backend intelligence is introduced here.
"""

import math
import sys
from datetime import datetime

import psutil
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import (
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.brain.brain import Brain
from src.core.orchestrator import Orchestrator
from src.voice.voice_manager import VoiceManager


# ============================================================
# COLORS
# ============================================================

BG = "#020711"
BG_2 = "#04101c"
PANEL = "#061525"
PANEL_2 = "#081b2a"
CYAN = "#24dfff"
CYAN_2 = "#0ba8ff"
BLUE = "#1578ff"
GREEN = "#3cff9b"
ORANGE = "#ffb84a"
RED = "#ff5268"
TEXT = "#dffbff"
MUTED = "#6f9bab"
LINE = "#123c55"


# ============================================================
# CUSTOM AURA CORE
# ============================================================

class AuraCoreWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.phase = 0.0
        self.listening = False
        self.thinking = False
        self.setMinimumSize(360, 320)

    def set_state(self, listening=False, thinking=False):
        self.listening = listening
        self.thinking = thinking
        self.update()

    def tick(self):
        self.phase += 0.035
        if self.phase > math.tau:
            self.phase = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        cx = w / 2
        cy = h / 2 - 10
        base = min(w, h) * 0.145

        # Deep background
        painter.fillRect(self.rect(), QColor(BG))

        # Futuristic grid
        painter.setPen(QPen(QColor("#082235"), 1))
        for x in range(0, w, 32):
            painter.drawLine(x, 0, x, h)
        for y in range(0, h, 32):
            painter.drawLine(0, y, w, y)

        # Horizon
        horizon = int(cy + base * 1.65)
        painter.setPen(QPen(QColor("#0c4560"), 1))
        painter.drawLine(0, horizon, w, horizon)

        # Floor perspective lines
        for i in range(-8, 9):
            x = cx + i * 34
            painter.drawLine(int(cx), horizon, int(x * 1.9 - cx * 0.9), h)

        # Outer orbital rings
        pulse = math.sin(self.phase * 2) * 7
        for multiplier, alpha in ((1.95, 90), (1.72, 120), (1.48, 150)):
            radius = base * multiplier + pulse
            pen = QPen(QColor(36, 223, 255, alpha), 2)
            painter.setPen(pen)
            painter.drawEllipse(
                QRectF(cx - radius, cy - radius, radius * 2, radius * 2)
            )

        # Segmented orbit
        painter.setPen(QPen(QColor(CYAN_2), 3))
        radius = base * 1.28
        start = int((self.phase * 180 / math.pi) * 16)
        painter.drawArc(
            QRectF(cx - radius, cy - radius, radius * 2, radius * 2),
            start,
            105 * 16,
        )
        painter.drawArc(
            QRectF(cx - radius, cy - radius, radius * 2, radius * 2),
            start + 180 * 16,
            72 * 16,
        )

        # Glow layers
        for scale, alpha in ((1.15, 24), (1.0, 38), (0.86, 65)):
            r = base * scale
            painter.setBrush(QColor(36, 223, 255, alpha))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QRectF(cx - r, cy - r, r * 2, r * 2))

        # Core
        core_gradient = QLinearGradient(
            cx - base, cy - base, cx + base, cy + base
        )
        core_gradient.setColorAt(0, QColor("#0b4b70"))
        core_gradient.setColorAt(0.45, QColor("#0b2033"))
        core_gradient.setColorAt(1, QColor("#02070d"))

        painter.setBrush(core_gradient)
        painter.setPen(QPen(QColor(CYAN), 3))
        r = base * 0.72
        painter.drawEllipse(QRectF(cx - r, cy - r, r * 2, r * 2))

        # Inner ring
        painter.setNoPen()
        painter.setBrush(QColor(36, 223, 255, 35))
        r2 = base * 0.48
        painter.drawEllipse(QRectF(cx - r2, cy - r2, r2 * 2, r2 * 2))

        # Center text
        painter.setPen(QColor(CYAN))
        font = QFont("Arial", max(18, int(base * 0.25)), QFont.Bold)
        painter.setFont(font)
        painter.drawText(
            QRectF(cx - base, cy - 20, base * 2, 40),
            Qt.AlignCenter,
            "AURA",
        )



# ============================================================
# MAIN WINDOW
# ============================================================

class AuraHUD(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AURA AI - Command Center")
        self.resize(1600, 950)
        self.setMinimumSize(1200, 760)
        self.is_hud_fullscreen = False

        # Existing backend
        self.brain = Brain()
        self.orchestrator = Orchestrator(self.brain)
        self.voice = VoiceManager()

        self.activity_lines = []
        self.conversation_lines = []

        self.build_ui()
        self.build_timers()
        self.showMaximized()

        self.log_activity("AURA initialized.")
        self.log_activity("Command center online.")
        self.log_activity("Awaiting user command...")
        self.add_aura_message("Hello! I am AURA AI.\nHow can I help you today?")

    # ========================================================
    # UI BUILD
    # ========================================================

    def build_ui(self):
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(8)

        layout.addWidget(self.build_top_bar())

        body = QHBoxLayout()
        body.setSpacing(8)

        body.addWidget(self.build_sidebar(), 0)
        body.addWidget(self.build_main_area(), 1)
        body.addWidget(self.build_right_area(), 0)

        layout.addLayout(body, 1)
        layout.addWidget(self.build_voice_bar())

        self.apply_theme()

    def build_top_bar(self):
        bar = QFrame()
        bar.setObjectName("topBar")
        row = QHBoxLayout(bar)
        row.setContentsMargins(12, 5, 12, 5)

        logo = QLabel("◉  AURA AI")
        logo.setObjectName("topLogo")
        row.addWidget(logo)

        row.addStretch()

        slogan = QLabel("A SMARTER YOU, A BRIGHTER TOMORROW.")
        slogan.setObjectName("slogan")
        row.addWidget(slogan)

        row.addStretch()

        self.user_label = QLabel("●  Hello, Amol")
        self.user_label.setObjectName("topInfo")
        row.addWidget(self.user_label)

        self.date_label = QLabel()
        self.date_label.setObjectName("topInfo")
        row.addWidget(self.date_label)

        self.time_label = QLabel()
        self.time_label.setObjectName("topInfo")
        row.addWidget(self.time_label)

        fullscreen = QPushButton("⛶")
        fullscreen.setObjectName("hudButton")
        fullscreen.setToolTip("Toggle fullscreen HUD")
        fullscreen.clicked.connect(self.toggle_hud_fullscreen)
        row.addWidget(fullscreen)

        return bar

    def build_sidebar(self):
        panel = QFrame()
        panel.setObjectName("sidebar")
        panel.setMinimumWidth(225)
        panel.setMaximumWidth(235)

        col = QVBoxLayout(panel)
        col.setContentsMargins(10, 12, 10, 10)
        col.setSpacing(5)

        brand = QLabel("◉")
        brand.setObjectName("brandOrb")
        brand.setAlignment(Qt.AlignCenter)
        col.addWidget(brand)

        aura = QLabel("AURA")
        aura.setObjectName("sideAura")
        aura.setAlignment(Qt.AlignCenter)
        col.addWidget(aura)

        sub = QLabel("ARTIFICIAL INTELLIGENCE\nCOMMAND CENTER")
        sub.setObjectName("sideSub")
        sub.setAlignment(Qt.AlignCenter)
        col.addWidget(sub)

        col.addSpacing(14)

        items = [
            ("HOME", "HOME"),
            ("CHAT", "CHAT"),
            ("VOICE", "VOICE"),
            ("VISION", "VISION"),
            ("MEMORY", "MEMORY"),
            ("WEB", "BROWSER"),
            ("APPS", "APPS"),
            ("TOOLS", "TOOLS"),
            ("SET", "SETTINGS"),
        ]

        for icon, name in items:
            button = QPushButton(f"▸  {name}")
            button.setObjectName("navButton")
            button.setCursor(Qt.PointingHandCursor)

            if name == "HOME":
                button.setProperty("active", True)

            if name == "CHAT":
                button.clicked.connect(lambda: self.command.setFocus())
            elif name == "VOICE":
                button.clicked.connect(self.process_voice_command)

            col.addWidget(button)

        col.addStretch()

        quote = QLabel(
            '"Discipline Today,\nA Brighter Tomorrow."\n\n— AURA'
        )
        quote.setObjectName("quote")
        quote.setAlignment(Qt.AlignCenter)
        col.addWidget(quote)

        version = QLabel("● AURA v0.82.0\n● SYSTEM SECURE")
        version.setObjectName("version")
        col.addWidget(version)

        return panel

    def build_main_area(self):
        panel = QWidget()
        col = QVBoxLayout(panel)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(8)

        upper = QHBoxLayout()
        upper.setSpacing(8)

        upper.addWidget(self.build_system_monitor(), 1)
        upper.addWidget(self.build_core_panel(), 2)
        upper.addWidget(self.build_status_panel(), 1)

        col.addLayout(upper, 1)
        col.addWidget(self.build_conversation(), 1)

        return panel

    def build_system_monitor(self):
        panel = self.card("SYSTEM MONITOR")
        col = panel.layout()

        gauges = QHBoxLayout()
        self.cpu_gauge = self.gauge("CPU")
        self.ram_gauge = self.gauge("RAM")
        self.disk_gauge = self.gauge("DISK")

        gauges.addWidget(self.cpu_gauge)
        gauges.addWidget(self.ram_gauge)
        gauges.addWidget(self.disk_gauge)

        col.addLayout(gauges)

        self.system_graph = QLabel("▁▂▃▄▂▅▇▃▂▄▆▅▃▇▆▄▅▂▃▅▇")
        self.system_graph.setObjectName("graphText")
        self.system_graph.setAlignment(Qt.AlignCenter)
        col.addWidget(self.system_graph)

        self.process_label = QLabel("PROCESSES     --")
        self.uptime_label = QLabel("UPTIME        LOCAL")
        self.network_label = QLabel("NETWORK       LIVE")
        self.monitor_state = QLabel("●  ALL SYSTEMS NOMINAL")

        for label in (
            self.process_label,
            self.uptime_label,
            self.network_label,
            self.monitor_state,
        ):
            label.setObjectName("metricLine")
            col.addWidget(label)

        return panel

    def build_core_panel(self):
        panel = self.card("AURA CORE")
        col = panel.layout()

        self.core = AuraCoreWidget()
        self.core.setMinimumHeight(250)
        self.core.setMaximumHeight(285)
        col.addWidget(self.core, 1)

        self.core_status = QLabel("ONLINE")
        self.core_status.setObjectName("bigStatus")
        self.core_status.setAlignment(Qt.AlignCenter)
        col.addWidget(self.core_status)

        self.core_detail = QLabel("SYSTEM READY   |   WAITING FOR COMMAND")
        self.core_detail.setObjectName("coreDetail")
        self.core_detail.setAlignment(Qt.AlignCenter)
        col.addWidget(self.core_detail)

        self.core_mode = QLabel("LISTEN   •   THINK   •   ANALYZE   •   RESPOND")
        self.core_mode.setObjectName("coreMode")
        self.core_mode.setAlignment(Qt.AlignCenter)
        col.addWidget(self.core_mode)

        self.core_signal = QLabel("◈  AURA NEURAL INTERFACE  ◈")
        self.core_signal.setObjectName("coreSignal")
        self.core_signal.setAlignment(Qt.AlignCenter)
        col.addWidget(self.core_signal)

        return panel

    def build_status_panel(self):
        panel = self.card("AI STATUS")
        col = panel.layout()

        statuses = [
            ("BRAIN", "READY", GREEN),
            ("MEMORY", "READY", GREEN),
            ("VOICE", "STANDBY", GREEN),
            ("VISION", "READY", GREEN),
            ("WEB", "READY", GREEN),
            ("DEVELOPER", "READY", GREEN),
            ("SECURITY", "LOCKED", RED),
        ]

        for name, value, color in statuses:
            row = QHBoxLayout()
            label = QLabel(f"●  {name}")
            label.setObjectName("statusName")
            value_label = QLabel(value)
            value_label.setObjectName("statusValue")
            value_label.setStyleSheet(f"color:{color};")

            row.addWidget(label)
            row.addStretch()
            row.addWidget(value_label)
            col.addLayout(row)

        return panel

    def build_conversation(self):
        panel = self.card("AURA CONVERSATION")
        col = panel.layout()

        header = QHBoxLayout()
        model = QLabel("MODEL: AURA BRAIN v1.0   |   MODE: ASSISTANT")
        model.setObjectName("miniInfo")
        header.addWidget(model)
        header.addStretch()

        for text in ("CHAT", "VOICE", "VISION", "CODE", "APPS"):
            b = QPushButton(text)
            b.setObjectName("miniButton")
            if text == "VOICE":
                b.clicked.connect(self.process_voice_command)
            header.addWidget(b)

        col.addLayout(header)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setObjectName("chatConsole")
        col.addWidget(self.chat, 2)

        quick = QHBoxLayout()
        quick_items = [
            "What can you do?",
            "Open Chrome",
            "Today's date",
            "My name is?",
            "System status",
        ]

        for item in quick_items:
            b = QPushButton(item)
            b.setObjectName("quickButton")
            b.clicked.connect(lambda checked=False, text=item: self.quick_command(text))
            quick.addWidget(b)

        col.addLayout(quick)

        command_row = QHBoxLayout()

        icon = QLabel("◉")
        icon.setObjectName("inputOrb")
        command_row.addWidget(icon)

        self.command = QLineEdit()
        self.command.setObjectName("commandInput")
        self.command.setPlaceholderText(
            "Type your command here... (e.g. hello, what time is it, open chrome)"
        )
        self.command.returnPressed.connect(self.process_command)
        command_row.addWidget(self.command, 1)

        attach = QPushButton("⌕")
        attach.setObjectName("inputButton")
        command_row.addWidget(attach)

        mic = QPushButton("♩")
        mic.setObjectName("inputButton")
        mic.clicked.connect(self.process_voice_command)
        command_row.addWidget(mic)

        send = QPushButton("➤")
        send.setObjectName("sendButton")
        send.clicked.connect(self.process_command)
        command_row.addWidget(send)

        col.addLayout(command_row)

        return panel

    def build_right_area(self):
        panel = QWidget()
        panel.setMinimumWidth(320)
        panel.setMaximumWidth(360)

        col = QVBoxLayout(panel)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(8)

        time_card = self.card("DATE & TIME")
        time_col = time_card.layout()

        self.big_clock = QLabel("00:00:00")
        self.big_clock.setObjectName("bigClock")
        time_col.addWidget(self.big_clock)

        self.big_date = QLabel()
        self.big_date.setObjectName("dateText")
        time_col.addWidget(self.big_date)

        location = QLabel("⌖  LOCAL SYSTEM")
        location.setObjectName("locationText")
        time_col.addWidget(location)

        col.addWidget(time_card)

        activity_card = self.card("ACTIVITY LOG")
        activity_col = activity_card.layout()

        self.activity = QTextEdit()
        self.activity.setReadOnly(True)
        self.activity.setObjectName("activityConsole")
        activity_col.addWidget(self.activity, 1)

        clear = QPushButton("CLEAR")
        clear.setObjectName("clearButton")
        clear.clicked.connect(self.clear_activity)
        activity_col.addWidget(clear)

        col.addWidget(activity_card, 1)

        tools = self.card("QUICK TOOLS")
        tools_col = tools.layout()

        tool_row = QHBoxLayout()
        tools_list = [
            ("CHROME", "open chrome"),
            ("NOTEPAD", "open notepad"),
            ("CALC", "open calculator"),
            ("SCREEN", "take screenshot"),
        ]

        for name, command in tools_list:
            b = QPushButton(name)
            b.setObjectName("toolButton")
            b.clicked.connect(
                lambda checked=False, cmd=command: self.quick_command(cmd)
            )
            tool_row.addWidget(b)

        tools_col.addLayout(tool_row)
        col.addWidget(tools)

        return panel

    def build_voice_bar(self):
        bar = QFrame()
        bar.setObjectName("voiceBar")
        row = QHBoxLayout(bar)
        row.setContentsMargins(12, 7, 12, 7)

        title = QLabel("◉  VOICE COMMAND")
        title.setObjectName("voiceTitle")
        row.addWidget(title)

        self.wave = QLabel(
            "▁▂▃▅▇▅▃▂▅▇▆▄▂▃▆▇▅▃▂▅▆▇▅▃▂"
        )
        self.wave.setObjectName("wave")
        row.addWidget(self.wave, 1)

        self.voice_status = QLabel("STATUS: STANDBY")
        self.voice_status.setObjectName("voiceStatus")
        row.addWidget(self.voice_status)

        listen = QPushButton("♩  LISTEN")
        listen.setObjectName("listenButton")
        listen.clicked.connect(self.process_voice_command)
        row.addWidget(listen)

        return bar

    # ========================================================
    # WIDGET HELPERS
    # ========================================================

    def card(self, title):
        frame = QFrame()
        frame.setObjectName("card")

        col = QVBoxLayout(frame)
        col.setContentsMargins(10, 9, 10, 9)
        col.setSpacing(7)

        heading = QLabel(title)
        heading.setObjectName("cardTitle")
        col.addWidget(heading)

        return frame

    def gauge(self, name):
        label = QLabel(f"{name}\n--%")
        label.setObjectName("gauge")
        label.setAlignment(Qt.AlignCenter)
        return label

    # ========================================================
    # COMMANDS
    # ========================================================

    def quick_command(self, command):
        self.command.setText(command)
        self.process_command()

    def process_command(self):
        command = self.command.text().strip()
        if not command:
            return

        self.command.clear()
        self.core.set_state(thinking=True)
        self.core_status.setText("THINKING")
        self.core_detail.setText("PROCESSING REQUEST")
        self.core_mode.setText("LISTEN   •   THINKING   •   ANALYZE   •   RESPOND")
        self.voice_status.setText("STATUS: THINKING")

        self.add_user_message(command)
        self.log_activity(f"USER: {command}")

        try:
            response = self.orchestrator.handle(command)
            self.add_aura_message(str(response))
            self.log_activity(f"AURA: {response}")

        except Exception as exc:
            self.add_aura_message(f"Error: {exc}")
            self.log_activity(f"ERROR: {exc}")

        finally:
            self.set_ready()

    def process_voice_command(self):
        self.core.set_state(listening=True)
        self.core_status.setText("LISTENING")
        self.core_detail.setText("SPEAK NOW")
        self.core_mode.setText("LISTENING   •   CAPTURING VOICE   •   THINK")
        self.voice_status.setText("STATUS: LISTENING")
        self.log_activity("Voice input activated.")

        try:
            command = self.voice.listen()

            if not command:
                self.log_activity("No voice command detected.")
                return

            self.add_user_message(f"🎤 {command}")
            self.log_activity(f"VOICE: {command}")

            self.core.set_state(thinking=True)
            self.core_status.setText("THINKING")
            response = self.orchestrator.handle(command)

            self.add_aura_message(str(response))
            self.log_activity(f"AURA: {response}")

            self.voice_status.setText("STATUS: SPEAKING")
            self.voice.speak(response)

        except Exception as exc:
            self.add_aura_message(f"Voice error: {exc}")
            self.log_activity(f"VOICE ERROR: {exc}")

        finally:
            self.set_ready()

    # ========================================================
    # CHAT / ACTIVITY
    # ========================================================

    def add_user_message(self, text):
        self.conversation_lines.append(("USER", text))
        self.refresh_chat()

    def add_aura_message(self, text):
        self.conversation_lines.append(("AURA", text))
        self.refresh_chat()

    def refresh_chat(self):
        html = []
        for speaker, text in self.conversation_lines[-20:]:
            safe = (
                str(text)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br>")
            )

            if speaker == "USER":
                html.append(
                    f'<div style="margin:10px 5px; color:#dffbff; '
                    f'background:#0a3150; padding:10px; '
                    f'border:1px solid #12608a; border-radius:8px;">'
                    f'<b>YOU</b><br>{safe}</div>'
                )
            else:
                html.append(
                    f'<div style="margin:10px 5px; color:#dffbff; '
                    f'background:#071d2c; padding:10px; '
                    f'border:1px solid #0b7fa8; border-radius:8px;">'
                    f'<b style="color:#24dfff;">AURA</b><br>{safe}</div>'
                )

        self.chat.setHtml("".join(html))
        self.chat.verticalScrollBar().setValue(
            self.chat.verticalScrollBar().maximum()
        )

    def log_activity(self, message):
        self.activity_lines.append(message)
        self.activity_lines = self.activity_lines[-40:]

        lines = []
        for index, item in enumerate(self.activity_lines, 1):
            lines.append(f"[{index:02d}] {item}")

        self.activity.setPlainText("\n".join(lines))
        self.activity.verticalScrollBar().setValue(
            self.activity.verticalScrollBar().maximum()
        )

    def clear_activity(self):
        self.activity_lines.clear()
        self.activity.clear()
        self.log_activity("Activity log cleared.")

    # ========================================================
    # SYSTEM
    # ========================================================

    def update_system(self):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent
            processes = len(psutil.pids())

            self.cpu_gauge.setText(f"CPU\n{cpu:.0f}%")
            self.ram_gauge.setText(f"RAM\n{ram:.0f}%")
            self.disk_gauge.setText(f"DISK\n{disk:.0f}%")

            self.process_label.setText(f"PROCESSES     {processes}")
            self.uptime_label.setText("UPTIME        ACTIVE")
            self.network_label.setText("NETWORK       LIVE")

            samples = int(cpu / 5)
            pattern = "▁▂▃▅▇▅▃▂▅▇▆▄▂▃▆▇▅▃▂▅▆▇▅▃▂"
            self.system_graph.setText(pattern[: max(8, min(25, 8 + samples))])

        except Exception:
            pass

    def update_clock(self):
        now = datetime.now()
        self.time_label.setText(now.strftime("%H:%M:%S"))
        self.date_label.setText(now.strftime("%A, %d %b %Y"))
        self.big_clock.setText(now.strftime("%I:%M:%S %p"))
        self.big_date.setText(now.strftime("%A, %d %B %Y"))

    def animate(self):
        self.core.tick()

        signal = [
            "◈  AURA NEURAL INTERFACE  ◈",
            "◈  SYNCHRONIZED  •  ONLINE  ◈",
            "◈  COGNITIVE CORE  •  READY  ◈",
        ][int(datetime.now().microsecond / 100000) % 3]
        self.core_signal.setText(signal)

        now = datetime.now()
        phase = int(now.microsecond / 100000)

        waves = [
            "▁▂▃▅▇▅▃▂▅▇▆▄▂▃▆▇▅▃▂▅▆▇▅▃▂",
            "▂▃▅▇▅▃▂▅▇▆▄▂▃▆▇▅▃▂▅▆▇▅▃▂▁",
            "▃▅▇▅▃▂▅▇▆▄▂▃▆▇▅▃▂▅▆▇▅▃▂▁▂",
        ]
        self.wave.setText(waves[phase % len(waves)])

    def set_ready(self):
        self.core.set_state()
        self.core_status.setText("ONLINE")
        self.core_detail.setText("SYSTEM READY   |   WAITING FOR COMMAND")
        self.core_mode.setText("LISTEN   •   THINK   •   ANALYZE   •   RESPOND")
        self.voice_status.setText("STATUS: STANDBY")

    def build_timers(self):
        self.system_timer = QTimer(self)
        self.system_timer.timeout.connect(self.update_system)
        self.system_timer.start(1500)

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.start(90)

        self.update_system()
        self.update_clock()

    # ========================================================
    # THEME
    # ========================================================

    def apply_theme(self):
        self.setStyleSheet(
            f"""
            QMainWindow, QWidget#root {{
                background: {BG};
                color: {TEXT};
                font-family: Arial;
            }}

            QFrame#topBar {{
                background: #030b14;
                border-bottom: 1px solid #0b5877;
            }}

            QLabel#topLogo {{
                color: {CYAN};
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 2px;
            }}

            QLabel#slogan {{
                color: {CYAN_2};
                font-size: 10px;
                font-weight: bold;
                letter-spacing: 2px;
            }}

            QLabel#topInfo {{
                color: {TEXT};
                padding: 4px 10px;
                border-left: 1px solid {LINE};
            }}

            QFrame#sidebar,
            QFrame#card,
            QFrame#voiceBar {{
                background: rgba(6, 21, 37, 235);
                border: 1px solid #0b5d7c;
                border-radius: 6px;
            }}

            QLabel#brandOrb {{
                color: {CYAN};
                font-size: 54px;
                padding-top: 3px;
            }}

            QLabel#sideAura {{
                color: {CYAN};
                font-size: 31px;
                font-weight: bold;
                letter-spacing: 6px;
            }}

            QLabel#sideSub {{
                color: {MUTED};
                font-size: 8px;
                letter-spacing: 1px;
            }}

            QPushButton#navButton {{
                background: transparent;
                color: #8edcff;
                border: 1px solid transparent;
                text-align: left;
                padding: 10px 12px;
                font-size: 11px;
                min-height: 38px;
                border-radius: 3px;
            }}

            QPushButton#navButton:hover,
            QPushButton#navButton[active="true"] {{
                background: #073354;
                color: {CYAN};
                border: 1px solid {CYAN_2};
            }}

            QLabel#quote {{
                color: #80cfe7;
                font-size: 11px;
                font-style: italic;
                padding: 10px;
            }}

            QLabel#version {{
                color: {GREEN};
                font-family: Consolas;
                font-size: 9px;
                padding: 5px;
            }}

            QLabel#cardTitle {{
                color: {CYAN};
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 1px;
                padding-bottom: 6px;
                border-bottom: 1px solid #0b4560;
            }}

            QLabel#gauge {{
                background: #03101c;
                border: 2px solid #0d4e6c;
                border-radius: 42px;
                color: {TEXT};
                font-family: Consolas;
                font-size: 11px;
                font-weight: bold;
                min-width: 72px;
                min-height: 72px;
            }}

            QLabel#graphText {{
                color: {CYAN};
                background: #03101a;
                border: 1px solid #0b4560;
                padding: 7px;
                font-family: Consolas;
            }}

            QLabel#metricLine {{
                color: #9bd4e5;
                font-family: Consolas;
                padding: 4px;
            }}

            QLabel#bigStatus {{
                color: {CYAN};
                font-size: 24px;
                font-weight: bold;
                letter-spacing: 7px;
                padding-top: 3px;
            }}

            QLabel#coreDetail {{
                color: {MUTED};
                font-family: Consolas;
                font-size: 10px;
            }}

            QLabel#coreMode {{
                color: #1b86b1;
                font-family: Consolas;
                font-size: 8px;
                letter-spacing: 2px;
                padding-top: 4px;
            }}

            QLabel#coreSignal {{
                color: #16779d;
                font-family: Consolas;
                font-size: 7px;
                letter-spacing: 3px;
                padding-top: 2px;
            }}

            QLabel#monitorState {{
                color: {GREEN};
                font-family: Consolas;
                font-size: 9px;
                padding: 7px 4px;
                border-top: 1px solid #0b4560;
            }}

            QPushButton#hudButton {{
                background: #041522;
                color: {CYAN};
                border: 1px solid #0b5877;
                min-width: 32px;
                padding: 4px 8px;
                font-size: 12px;
            }}

            QPushButton#hudButton:hover {{
                background: {CYAN};
                color: {BG};
            }}

            QLabel#statusName {{
                color: {TEXT};
                padding: 6px;
                border-bottom: 1px solid #0b3045;
            }}

            QLabel#statusValue {{
                font-family: Consolas;
                padding: 6px;
            }}

            QTextEdit#chatConsole,
            QTextEdit#activityConsole {{
                background: #020b14;
                border: 1px solid #0b4560;
                color: {TEXT};
                font-family: Consolas;
                font-size: 10px;
            }}

            QLabel#miniInfo {{
                color: {MUTED};
                font-family: Consolas;
                font-size: 9px;
            }}

            QPushButton#miniButton,
            QPushButton#quickButton,
            QPushButton#toolButton {{
                background: #061a29;
                color: #9edff1;
                border: 1px solid #0b5877;
                padding: 7px 9px;
                border-radius: 4px;
                font-size: 9px;
            }}

            QPushButton#miniButton:hover,
            QPushButton#quickButton:hover,
            QPushButton#toolButton:hover {{
                background: #0b3c5a;
                color: {CYAN};
                border: 1px solid {CYAN};
            }}

            QLabel#inputOrb {{
                color: {CYAN};
                font-size: 27px;
            }}

            QLineEdit#commandInput {{
                background: #020b14;
                color: {TEXT};
                border: 1px solid #0b5877;
                padding: 10px;
                font-family: Consolas;
                font-size: 10px;
            }}

            QLineEdit#commandInput:focus {{
                border: 1px solid {CYAN};
            }}

            QPushButton#inputButton {{
                background: #061a29;
                color: {CYAN};
                border: 1px solid #0b5877;
                padding: 9px 13px;
            }}

            QPushButton#sendButton {{
                background: #0878c7;
                color: white;
                border: 1px solid {CYAN};
                padding: 9px 18px;
                font-size: 17px;
                font-weight: bold;
            }}

            QPushButton#sendButton:hover {{
                background: #13a6ff;
            }}

            QLabel#bigClock {{
                color: #a7ddff;
                font-size: 28px;
                font-weight: bold;
            }}

            QLabel#dateText {{
                color: {MUTED};
                font-size: 11px;
            }}

            QLabel#locationText {{
                color: {CYAN};
                padding-top: 5px;
            }}

            QPushButton#clearButton {{
                background: transparent;
                color: {MUTED};
                border: 1px solid #0b4560;
                padding: 5px;
            }}

            QLabel#voiceTitle {{
                color: {CYAN};
                font-weight: bold;
                letter-spacing: 1px;
            }}

            QLabel#wave {{
                color: {CYAN};
                font-size: 17px;
                font-family: Consolas;
                letter-spacing: 1px;
            }}

            QLabel#voiceStatus {{
                color: {GREEN};
                font-family: Consolas;
                font-size: 9px;
            }}

            QPushButton#listenButton {{
                background: #05283c;
                color: {CYAN};
                border: 1px solid {CYAN};
                padding: 8px 18px;
                font-weight: bold;
                border-radius: 4px;
            }}

            QPushButton#listenButton:hover {{
                background: {CYAN};
                color: {BG};
            }}

            QScrollBar:vertical {{
                background: #020a12;
                width: 8px;
            }}

            QScrollBar::handle:vertical {{
                background: #0b5877;
                min-height: 30px;
            }}
            """
        )

    def toggle_hud_fullscreen(self):
        if self.isFullScreen():
            self.showMaximized()
            self.is_hud_fullscreen = False
        else:
            self.showFullScreen()
            self.is_hud_fullscreen = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            self.toggle_hud_fullscreen()
            return
        super().keyPressEvent(event)

    def closeEvent(self, event):
        try:
            self.system_timer.stop()
            self.clock_timer.stop()
            self.animation_timer.stop()
        except Exception:
            pass
        event.accept()


def launch():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    window = AuraHUD()
    window.show()
    return app.exec()


if __name__ == "__main__":
    launch()
