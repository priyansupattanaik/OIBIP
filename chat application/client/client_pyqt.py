import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QTextCursor
import os

class ChatClient(QWidget):
    message_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.client_socket = None
        self.username = None
        self.chatroom = None

    def init_ui(self):
        self.setWindowTitle("Chat Application")

        self.layout = QVBoxLayout()

        self.username_label = QLabel("Username")
        self.layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        self.layout.addWidget(self.username_input)

        self.chatroom_label = QLabel("Chatroom")
        self.layout.addWidget(self.chatroom_label)
        self.chatroom_input = QLineEdit()
        self.layout.addWidget(self.chatroom_input)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_server)
        self.layout.addWidget(self.connect_button)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.layout.addWidget(self.text_area)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Enter your message...")
        self.message_input.returnPressed.connect(self.send_message)
        self.layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.file_button = QPushButton("Send File")
        self.file_button.clicked.connect(self.send_file)
        self.layout.addWidget(self.file_button)

        self.clear_button = QPushButton("Clear History")
        self.clear_button.clicked.connect(self.clear_history)
        self.layout.addWidget(self.clear_button)

        self.setLayout(self.layout)
        self.message_received.connect(self.display_message)

    def connect_to_server(self):
        self.username = self.username_input.text()
        self.chatroom = self.chatroom_input.text()

        if not self.username or not self.chatroom:
            QMessageBox.warning(self, "Input Error", "Please enter both username and chatroom.")
            return

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(("127.0.0.1", 12345))

            self.client_socket.send(self.username.encode('utf-8'))
            self.client_socket.recv(1024)  # Acknowledgement from server
            self.client_socket.send(self.chatroom.encode('utf-8'))
            self.client_socket.recv(1024)  # Acknowledgement from server

            self.connect_button.setDisabled(True)
            self.username_input.setDisabled(True)
            self.chatroom_input.setDisabled(True)
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", str(e))

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.message_received.emit(message)
            except ConnectionResetError:
                break

    def send_message(self):
        message = self.message_input.text()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.message_input.clear()
            self.display_message(f'{self.username}: {message}')

    def send_file(self):
        file_path = QFileDialog.getOpenFileName(self, "Select File")[0]
        if file_path:
            # For now, just display a message about the file
            self.display_message(f'File selected: {file_path}')

    def clear_history(self):
        self.text_area.clear()

    def display_message(self, message):
        self.text_area.append(message)
        self.text_area.moveCursor(QTextCursor.End)

    def closeEvent(self, event):
        if self.client_socket:
            self.client_socket.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    chat_client = ChatClient()
    chat_client.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
