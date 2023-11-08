from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QSizePolicy,\
    QScrollArea

from GUI import MemoDialog


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        textEdits = self._init_TextEdit()
        buttons = self._init_Button()

        self._init_Layout(buttons, textEdits)

        self.setWindowTitle('My First Application')
        self.setGeometry(300, 300, 300, 200)
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

    def _init_Button(self):
        self.sendButton = QPushButton('보내기')
        # TODO Socket Programming Integration

        self.memoButton = QPushButton('메모장')
        self.memoButton.clicked.connect(MemoDialog.init)

        self.exitButton = QPushButton('종료')
        self.exitButton.clicked.connect(self._exitApplication)
        return [self.sendButton, self.memoButton, self.exitButton]

    def _init_TextEdit(self):
        self.textInputEdit = QTextEdit()
        self.textInputEdit.setFixedHeight(30)
        self.textInputEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.textReceiveEdit = QTextEdit()
        self.textReceiveEdit.setReadOnly(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.textReceiveEdit)
        return [self.textInputEdit, self.textReceiveEdit]

    # noinspection PyMethodMayBeStatic
    def _exitApplication(self):
        # TODO Close Socket Connection
        quit(0)

    def _updateTextEdit(self, textEdit):
        # TODO Clear TextInputEdit after sending a message
        # TODO Update TextReceiveEdit with Socket Programming
        pass
