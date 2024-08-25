# Client-Client Chat with ktinker (GUI)

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import font

SERVER = "127.0.0.1"
HEADER = 64
PORT = 5454
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "bye"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

client_name = "Teja"

def send_message(event = None):
    message = message_entry.get()
    if message:
        chat_display.config(state = tk.NORMAL)
        chat_display.insert(tk.END, f"You: {message}\n", "sent")
        chat_display.yview(tk.END)
        message_entry.delete(0, tk.END)

        message_to_send = f"{client_name}: {message}".encode(FORMAT)
        msg_length = len(message_to_send)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client_socket.send(send_length)
        client_socket.send(message_to_send)

        if message == DISCONNECT_MESSAGE:
            client_socket.close()
            window.quit()

def receive_messages():
    while True:
        message = client_socket.recv(1024).decode(FORMAT)
        if message:
            chat_display.config(state = tk.NORMAL)
            chat_display.insert(tk.END, f"{message}\n", "received")
            chat_display.yview(tk.END)
            chat_display.config(state=tk.DISABLED)

window = tk.Tk()
window.title("Client - Client Chat")
window.geometry("500x500")
window.resizable(False, False)

window.configure(bg = "#2C3E50")

calibri_font = font.Font(family = "Calibri", size=11)

chat_display = scrolledtext.ScrolledText(window, state = tk.DISABLED, width = 60, height = 15, wrap = tk.WORD, bg = "#34495E", fg = "#ECF0F1", font = calibri_font, highlightthickness = 0)
chat_display.tag_config("sent", foreground = "#1ABC9C")
chat_display.tag_config("received", foreground = "#E74C3C")
chat_display.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2)

message_entry = tk.Entry(window, width = 45, bg = "#34495E", fg = "#ECF0F1", font = calibri_font, insertbackground = "#ECF0F1", highlightthickness = 0)
message_entry.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "w")

send_button = tk.Button(window, text = "Send", command = send_message, width = 10, bg = "#1ABC9C", fg = "#ECF0F1", font=calibri_font, bd = 0, highlightthickness = 0, activebackground = "#16A085", activeforeground = "#ECF0F1")
send_button.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = "e")

message_entry.bind("<Return>", send_message)

receive_thread = threading.Thread(target = receive_messages)
receive_thread.daemon = True
receive_thread.start()

window.mainloop()
