import socket
import tkinter as tk
from tkinter import scrolledtext
import threading

SERVER_IP = '127.0.0.1'
SERVER_PORT = 9000

class ClientGUI:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Chat Client - {self.username}")

        self.text_area = scrolledtext.ScrolledText(root, width=40, height=10, state='disabled')
        self.text_area.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.message_entry = tk.Entry(root, width=30)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, pady=10)

        self.quit_button = tk.Button(root, text="Quit", command=self.close_client)
        self.quit_button.grid(row=2, column=1, pady=10)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_IP, SERVER_PORT))

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

        # 엔터키 바인딩
        self.message_entry.bind('<Return>', lambda event: self.send_message())
        # Escape 키 바인딩
        self.root.bind('<Escape>', lambda event: self.close_client())

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                message = data.decode()
                self.display_message(message)

            except Exception as e:
                print(f"Error: {e}")
                break

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + '\n')
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')

    def send_message(self, event=None):  # 엔터키로 호출 시 event 매개변수 추가
        message = self.message_entry.get()
        if message:
            full_message = f"{self.username}: {message}"
            self.client_socket.sendall(full_message.encode())
            self.display_message(full_message)  # Display the sent message locally
            self.message_entry.delete(0, tk.END)

    def close_client(self, event=None):  # Escape 키로 호출 시 event 매개변수 추가
        self.client_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    username = input("Enter your username: ")
    root = tk.Tk()
    client_gui = ClientGUI(root, username)
    root.mainloop()
