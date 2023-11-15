import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

SERVER_IP = '127.0.0.1'
SERVER_PORT = 9000

clients = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Server")

        self.text_area = scrolledtext.ScrolledText(root, width=40, height=10, state='disabled')
        self.text_area.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.quit_button = tk.Button(root, text="Quit", command=self.close_server)
        self.quit_button.grid(row=1, column=1, pady=10)

        threading.Thread(target=self.accept_clients).start()

    def accept_clients(self):
        while True:
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)

            message = f"Client {client_address} has joined."
            self.display_message(message)

            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
            

    def handle_client(self, client_socket, client_address):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break

                message = f"Client {client_address}: {data.decode()}"
                self.display_message(message)

                for c in clients:
                    if c != client_socket:
                        c.sendall(data)

            except Exception as e:
                print(f"Error: {e}")
                break

        clients.remove(client_socket)
        client_socket.close()

        message = f"Client {client_address} has left."
        self.display_message(message)

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + '\n')
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')

    def close_server(self):
        for client in clients:
            client.close()
        server_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    server_gui = ServerGUI(root)
    root.mainloop()
