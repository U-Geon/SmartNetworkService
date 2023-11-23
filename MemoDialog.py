from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QDialog


# noinspection PyAttributeOutsideInit
class MemoDialog(QDialog):
    text = ""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.memoTextEdit = QTextEdit()
        self.setText(MemoDialog.text)
        self.memoTextEdit.moveCursor(QTextCursor.MoveOperation.End)
        vbox = QVBoxLayout()
        vbox.addWidget(self.memoTextEdit)

        self.setModal(False)
        self.setWindowTitle('메모장')
        self.setLayout(vbox)

        self.finished.connect(self.handleDialogFinished)

    def getText(self):
        return self.memoTextEdit.toPlainText()

    def setText(self, text):
        self.memoTextEdit.setPlainText(text)

    def handleDialogFinished(self):
        MemoDialog.text = self.getText()
        # print("Dialog closed with text:", MemoDialog.text)


def init():
    dialog = MemoDialog()
    dialog.show()
    result = dialog.exec_()

    # prev_text = dialog.getText()
    # dialog.setText(prev_text)
