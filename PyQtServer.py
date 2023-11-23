import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit
from PyQt5.QtNetwork import QTcpServer, QHostAddress
from PyQt5.QtCore import QTextStream

class PyQtServer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.server = QTcpServer(self)
        self.server.listen(QHostAddress('127.0.0.1'), 9000)
        self.server.newConnection.connect(self.new_connection)

        self.clients = []  # Maintain a list of connected clients

        self.central_widget = QTextEdit(self)
        self.central_widget.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.central_widget)

        self.setCentralWidget(self.central_widget)
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Chat Server')

    def new_connection(self):
        client_socket = self.server.nextPendingConnection()
        client_socket.readyRead.connect(self.receive_message)

        # Add the new client to the list
        self.clients.append(client_socket)

    def receive_message(self):
        client_socket = self.sender()
        data = QTextStream(client_socket).readAll()
        self.broadcast_message(data, client_socket)

    def broadcast_message(self, message, sender_socket):
        message_bytes = message.encode()  # Encode the string to bytes

        for client_socket in self.clients:
            client_socket.write(message_bytes)

        self.display_message(message)

    def display_message(self, message):
        self.central_widget.append(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    server = PyQtServer()
    server.show()
    sys.exit(app.exec_())