import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, \
    QSizePolicy

import MemoDialog
from PyQtServer import PyQtServer


class PyQtClient(QWidget):
    def __init__(self, username):
        super().__init__()

        self.username = username

        self.socket = QTcpSocket(self)
        self.socket.connected.connect(self.connected)
        self.socket.readyRead.connect(self.receive_message)
        self.socket.error.connect(self.create_server)

        self.connect()

        self.ui_timer = QTimer(self)
        self.ui_timer.timeout.connect(self.check_connection_status)
        self.ui_timer.start(100)

    def connect(self):
        print("Connecting to host...")
        self.socket.connectToHost('127.0.0.1', 9000)

    def check_connection_status(self):
        # print(f"self.socket.state():{self.socket.state()}")
        if self.socket.state() == QTcpSocket.ConnectedState:
            # 연결이 성공하면 타이머 중지하고 UI 초기화 진행
            self.ui_timer.stop()
            self.initUI()

    def create_server(self):
        print("Failed to connect server. Creating new server...")
        self.server = PyQtServer()
        print("Done.")
        self.connect()


    def initUI(self):
        textEdits = self._init_TextEdit()
        buttons = self._init_Button()

        self._init_Layout(buttons, textEdits)

        self.setWindowTitle(f'Chat Client - {self.username}')
        self.setBaseSize(500, 200)
        self.show()


    def _init_Layout(self, buttons, textEdits):
        self.hbox = QHBoxLayout()
        for button in buttons:
            self.hbox.addWidget(button)

        self.vbox = QVBoxLayout()
        for textEditLayout in textEdits:
            self.vbox.addLayout(textEditLayout)

        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

    def _init_TextEdit(self):
        self.input_edit = QLineEdit()
        self.input_edit.setFixedHeight(30)
        self.input_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.input_vbox = QVBoxLayout()
        self.input_vbox.addWidget(self.input_edit)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.text_vbox = QVBoxLayout()
        self.text_vbox.addWidget(self.text_edit)

        return [self.input_vbox, self.text_vbox]

    def _init_Button(self):
        self.sendButton = QPushButton('보내기')
        self.sendButton.clicked.connect(self.send_message)

        self.memoButton = QPushButton('메모장')
        self.memoButton.clicked.connect(MemoDialog.init)

        self.exitButton = QPushButton('종료')
        self.exitButton.clicked.connect(self.close)
        return [self.sendButton, self.memoButton, self.exitButton]

    def connected(self):
        print('Connected to server')

    def receive_message(self):
        data = self.socket.readAll().data().decode('utf-8', 'ignore')
        self.display_message(data)

    def send_message(self):
        message = self.input_edit.text()
        if message:
            full_message = f"{self.username}: {message}"
            self.socket.write(full_message.encode('utf-8'))
            self.input_edit.clear()

    def display_message(self, message):
        self.text_edit.append(message)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Return):
            self.send_message()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    username = input("Enter your username: ")
    client = PyQtClient(username)
    client.show()
    sys.exit(app.exec_())