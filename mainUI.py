import sys
import websocket
import threading

from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QTextEdit, QLineEdit, QPushButton, QLabel
)


class SocietyCordUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SocietyCord")
        self.setGeometry(200, 100, 1100, 650)

        self.ws = None
        self.connected = False

        # ---------------- MAIN LAYOUT ---------------- #
        main_layout = QHBoxLayout(self)

        # ---------------- SIDEBAR ---------------- #
        self.sidebar = QListWidget()
        self.sidebar.addItem("# general")
        self.sidebar.addItem("# dev")
        self.sidebar.addItem("# gaming")
        self.sidebar.setFixedWidth(200)

        # ---------------- CHAT AREA ---------------- #
        chat_container = QVBoxLayout()

        self.title = QLabel("💬 # general")
        self.title.setStyleSheet("font-size: 16px; font-weight: bold; color: #c084fc;")

        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)

        # ---------------- INPUT ---------------- #
        input_container = QHBoxLayout()

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Message #general")

        self.send_btn = QPushButton("Send")

        input_container.addWidget(self.message_input)
        input_container.addWidget(self.send_btn)

        chat_container.addWidget(self.title)
        chat_container.addWidget(self.chat_box)
        chat_container.addLayout(input_container)

        chat_widget = QWidget()
        chat_widget.setLayout(chat_container)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(chat_widget)

        self.setLayout(main_layout)

        # ---------------- STYLE ---------------- #
        self.setStyleSheet("""
            QWidget {
                background-color: #0b0b10;
                color: white;
                font-family: Arial;
                font-size: 13px;
            }

            QListWidget {
                background-color: #111118;
                border: none;
                padding: 10px;
                color: #c084fc;
            }

            QListWidget::item {
                padding: 10px;
                border-radius: 6px;
            }

            QListWidget::item:selected {
                background-color: #7c3aed;
                color: white;
            }

            QTextEdit {
                background-color: #151522;
                border: none;
                padding: 10px;
                color: white;
                border-radius: 10px;
            }

            QLineEdit {
                background-color: #151522;
                border: 1px solid #2a2a35;
                border-radius: 10px;
                padding: 10px;
                color: white;
            }

            QPushButton {
                background-color: #7c3aed;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                color: white;
            }

            QPushButton:hover {
                background-color: #9333ea;
            }

            QPushButton:pressed {
                background-color: #5b21b6;
            }
        """)

        # ---------------- SIGNALS ---------------- #
        self.send_btn.clicked.connect(self.send_message)

        # connect websocket automatically
        self.connect_ws()

    # ---------------- CONNECT ---------------- #
    def connect_ws(self):
        SERVER_URL = "wss://YOUR_SERVER_URL/ws/mania828"

        def on_message(ws, message):
            self.chat_box.append(message)

        def on_close(ws, *args):
            self.chat_box.append("🔴 Disconnected")

        def on_error(ws, error):
            self.chat_box.append(f"⚠ Error: {error}")

        def on_open(ws):
            self.chat_box.append("🟢 Connected to SocietyCord")

        self.ws = websocket.WebSocketApp(
            SERVER_URL,
            on_message=on_message,
            on_close=on_close,
            on_error=on_error,
            on_open=on_open
        )

        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    # ---------------- SEND MESSAGE ---------------- #
    def send_message(self):
        msg = self.message_input.text().strip()
        if not msg:
            return

        if self.ws:
            try:
                self.ws.send(msg)
            except:
                self.chat_box.append("❌ Not connected")

        self.message_input.clear()


# ---------------- RUN ---------------- #
app = QApplication(sys.argv)
window = SocietyCordUI()
window.show()
sys.exit(app.exec())
