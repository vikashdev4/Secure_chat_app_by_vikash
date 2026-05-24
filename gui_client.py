import socket
import threading
import tkinter as tk
from encryption import encrypt, decrypt

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

# ---------- FUNCTIONS ----------

def receive():
    while True:
        try:
            msg = client.recv(1024)
            message = decrypt(msg)
            add_message(message, "left")
        except:
            break

def send():
    message = entry.get()
    if message.strip() == "":
        return

    add_message(message, "right")   # 👈 show own message

    client.send(encrypt(message))
    entry.delete(0, tk.END)

def add_message(msg, side):
    msg_frame = tk.Frame(chat_area, bg="#121212")

    if side == "right":
        lbl = tk.Label(msg_frame, text=msg, bg="#BB86FC",
                       fg="black", padx=10, pady=5,
                       font=("Arial", 11), wraplength=250)
        lbl.pack(anchor="e", padx=10, pady=5)
    else:
        lbl = tk.Label(msg_frame, text=msg, bg="#2b2b2b",
                       fg="white", padx=10, pady=5,
                       font=("Arial", 11), wraplength=250)
        lbl.pack(anchor="w", padx=10, pady=5)

    msg_frame.pack(fill=tk.BOTH)

    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

# ---------- GUI ----------

window = tk.Tk()
window.title("🔐 Secure Chat")
window.geometry("500x600")
window.config(bg="#121212")

canvas = tk.Canvas(window, bg="#121212", highlightthickness=0)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(window, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

chat_area = tk.Frame(canvas, bg="#121212")
canvas.create_window((0, 0), window=chat_area, anchor="nw")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

chat_area.bind("<Configure>", on_configure)

# Bottom input
bottom_frame = tk.Frame(window, bg="#121212")
bottom_frame.pack(fill=tk.X, padx=10, pady=10)

entry = tk.Entry(bottom_frame, font=("Arial", 12),
                 bg="#1e1e1e", fg="white",
                 insertbackground="white", bd=0)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)

send_btn = tk.Button(bottom_frame, text="Send",
                     bg="#BB86FC", fg="black",
                     command=send)
send_btn.pack(side=tk.RIGHT)

# Thread
thread = threading.Thread(target=receive)
thread.daemon = True
thread.start()

window.mainloop()