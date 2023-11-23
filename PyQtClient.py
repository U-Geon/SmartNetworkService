import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, \
    QSizePolicy, QScrollArea
from PyQt5.QtNetwork import QTcpSocket

import MemoDialog


class PyQtClient(QWidget):
    def __init__(self, username):
        super().__init__()

        self.username = username

        self.socket = QTcpSocket(self)
        self.socket.connected.connect(self.connected)
        self.socket.readyRead.connect(self.receive_message)

        self.initUI()
        self.socket.connectToHost('127.0.0.1', 9000)

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
        for textEdit in textEdits:
            self.vbox.addWidget(textEdit)

        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

    def _init_TextEdit(self):
        self.input_edit = QLineEdit()
        self.input_edit.setFixedHeight(30)
        self.input_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.installEventFilter(self)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.text_edit)
        return [self.input_edit, self.text_edit]

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