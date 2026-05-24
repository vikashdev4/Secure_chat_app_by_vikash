import socket
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog
import winsound
import os
from PIL import Image, ImageTk
from datetime import datetime

from encryption import encrypt, decrypt
from auth import login, register

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ---------------- SOCKET ----------------
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 12345))

username = None
imgs = []

# ---------------- AUTH SCREEN ----------------
def auth_screen():
    global username

    win = tk.Tk()
    win.title("Secure Chat Login/Register")
    win.geometry("700x420")
    win.config(bg="#0f172a")

    # ================= WELCOME SCREEN =================
       # ================= WELCOME SCREEN =================
    # ================= WELCOME SCREEN =================
    welcome = tk.Frame(win, bg="#0f172a")
    welcome.pack(fill="both", expand=True)

    theme_dark = True

    def toggle_theme():
        nonlocal theme_dark
        theme_dark = not theme_dark

        bg = "#0f172a" if theme_dark else "#f1f5f9"
        fg = "#38bdf8" if theme_dark else "#0f172a"

        welcome.config(bg=bg)
        btn.config(text="🌙" if theme_dark else "☀", bg=bg)

        def update_widgets(widget):
            for w in widget.winfo_children():

                if isinstance(w, tk.Button):
                    continue
                else:
                    try:
                        w.config(bg=bg)
                    except:
                     pass
                try:
                    w.config(fg=fg)
                except:
                    pass

                update_widgets(w)

        update_widgets(welcome)
        

    btn = tk.Button(
        welcome,
        text="🌙|☀",
        font=("Arial", 14, "bold"),
        bg="#1e293b",
        fg="white",
        command=toggle_theme
)

    btn.place(relx=1.0, x=-10, y=10, anchor="ne")

    # -------- LOGO --------
    logo_img = Image.open("logo.png")
    logo_img = logo_img.resize((150, 150), Image.LANCZOS)
    logo_img = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(welcome, image=logo_img, bg="#0f172a")
    logo_label.image = logo_img
    logo_label.pack(pady=(30,10))

    # -------- WELCOME TEXT --------
    tk.Label(
        welcome,
        text="WELCOME\nMITS SECURE CHAT SYSTEM",
        font=("Segoe UI", 36, "bold"),
        fg="#38bdf8",
        bg="#0f172a",
        justify="center"
    ).pack(pady=(20,10))

    # -------- TAGLINE --------
    tk.Label(
        welcome,
        text="Safe • Fast • Encrypted Chat System",
        font=("Segoe UI", 11),
        fg="#94a3b8",
        bg="#0f172a"
    ).pack(pady=5)

    # -------- INFO TEXT --------
    tk.Label(
        welcome,
        text="Click below to continue",
        font=("Arial", 14),
        fg="#f88b38",
        bg="#0f172a"
    ).pack(pady=10)

    # -------- BUTTON FUNCTION --------
    def open_login():
        welcome.destroy()
        show_login()

    # -------- BUTTON --------
    tk.Button(
        welcome,
        text="Get Started →",
        font=("Arial", 12, "bold"),
        bg="#22c55e",
        fg="white",
        activebackground="#16a34a",
        bd=0,
        cursor="hand2",
        padx=20,
        pady=5,
        command=open_login
        ).pack(pady=25)

    # -------- DEVELOPER SECTION --------
    dev_frame = tk.Frame(welcome, bg="#0f172a")
    dev_frame.pack(pady=12)

    # ---- PHOTO ----
    dev_img = Image.open("owner.jpg")
    dev_img = dev_img.resize((90, 90), Image.LANCZOS)
    dev_img = ImageTk.PhotoImage(dev_img)

    dev_label = tk.Label(dev_frame, image=dev_img, bg="#0f172a")
    dev_label.image = dev_img
    dev_label.pack(pady=(5,8))

    # ---- TEXT ----
    tk.Label(
        dev_frame,
        text="Developed by\nVikash Dhakad\nMAC, II Year",
        font=("Segoe UI", 10, "bold"),
        fg="#ffffff",   # 👈 best for blue background
        bg="#0f172a",
        justify="center"
    ).pack()

    # ================= LOGIN PAGE =================
    def show_login():

        # ---------------- HEADER ----------------
        top_frame = tk.Frame(win, bg="#0f172a")
        top_frame.pack(pady=10)

        logo_img = Image.open("logo.png")
        logo_img = logo_img.resize((100, 100))
        logo_img = ImageTk.PhotoImage(logo_img)

        logo_label = tk.Label(top_frame, image=logo_img, bg="#0f172a")
        logo_label.image = logo_img
        logo_label.pack(side="left", padx=10)

        title = tk.Label(
            top_frame,
            text="MITS Secure Chat System\nMadhav Institute of Technology & Science",
            font=("Arial", 20, "bold"),
            fg="yellow",
            bg="#0f172a"
        )
        title.pack(side="left")

        tk.Label(
            win,
            text="Safe • Fast • Encrypted Chat System",
            font=("Arial", 10),
            fg="#f83838",
            bg="#0f172a"
        ).pack(pady=5)

        # ---------------- MAIN ----------------
        main = tk.Frame(win, bg="#1e293b")
        main.pack(pady=25)

        # ================= LOGIN =================
        login_frame = tk.Frame(main, bg="#2563eb", width=280, height=260)
        login_frame.pack(side="left", padx=15, pady=15)
        login_frame.pack_propagate(False)

        tk.Label(login_frame, text="LOGIN", fg="white", bg="#2563eb",
                 font=("Arial", 16, "bold")).pack(pady=10)

        lu = tk.Entry(login_frame, font=("Arial", 12), bg="white", fg="black")
        lu.insert(0, "Username")
        lu.bind("<FocusIn>", lambda e: lu.delete(0, tk.END) if lu.get() == "Username" else None)
        lu.pack(pady=8, ipady=3)

        lp = tk.Entry(login_frame, show="*", font=("Arial", 12), bg="white", fg="black")
        lp.insert(0, "Password")
        lp.bind("<FocusIn>", lambda e: lp.delete(0, tk.END) if lp.get() == "Password" else None)
        lp.pack(pady=8, ipady=3)

        def do_login():
            global username
            u = lu.get()
            p = lp.get()

            if login(u, p):
                username = u
                win.destroy()
                start_chat()
            else:
                messagebox.showerror("Error", "Invalid Login")

        tk.Button(
            login_frame,
            text="LOGIN",
            bg="#22c55e",
            fg="white",
            font=("Arial", 12, "bold"),
            command=do_login
        ).pack(pady=15)

        # ================= REGISTER =================
        reg_frame = tk.Frame(main, bg="#7c3aed", width=280, height=260)
        reg_frame.pack(side="right", padx=15, pady=15)
        reg_frame.pack_propagate(False)

        tk.Label(reg_frame, text="REGISTER", fg="white", bg="#7c3aed",
                 font=("Arial", 16, "bold")).pack(pady=10)

        ru = tk.Entry(reg_frame, font=("Arial", 12), bg="white", fg="black")
        ru.insert(0, "Username")
        ru.bind("<FocusIn>", lambda e: ru.delete(0, tk.END) if ru.get() == "Username" else None)
        ru.pack(pady=8, ipady=3)

        rp = tk.Entry(reg_frame, show="*", font=("Arial", 12), bg="white", fg="black")
        rp.insert(0, "Password")
        rp.bind("<FocusIn>", lambda e: rp.delete(0, tk.END) if rp.get() == "Password" else None)
        rp.pack(pady=8, ipady=3)

        def do_register():
            u = ru.get()
            p = rp.get()

            if u.strip() and p.strip():
                register(u, p)
                messagebox.showinfo("Success", "Registered Successfully")
            else:
                messagebox.showerror("Error", "Fill all fields")

        tk.Button(
            reg_frame,
            text="REGISTER",
            bg="#f59e0b",
            fg="black",
            font=("Arial", 12, "bold"),
            command=do_register
        ).pack(pady=15)

    win.mainloop()


# ---------------- CHAT ----------------
def start_chat():
    global root, username, imgs

    root = tk.Tk()
    root.title(f"Secure Chat - {username}")
    root.geometry("700x600")
    root.config(bg="#e5ddd5")

    client.send(encrypt(username))

    frame = tk.Frame(root, bg="#e5ddd5")
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame, bg="#e5ddd5", highlightthickness=0)
    scroll = tk.Scrollbar(frame, command=canvas.yview)

    chat = tk.Frame(canvas, bg="#e5ddd5")

    canvas.create_window((0, 0), window=chat, anchor="nw")
    canvas.configure(yscrollcommand=scroll.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    chat.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    profiles = {}

    try:
        profiles["Vikash"] = ImageTk.PhotoImage(Image.open("vikash.jpg").resize((35,35)))
        profiles["Rahul"] = ImageTk.PhotoImage(Image.open("rahul.jpg").resize((35,35)))
    except:
        print("⚠ DP not found")

    def add(msg, sender):
        outer = tk.Frame(chat, bg="#e5ddd5")
        outer.pack(fill="x", pady=3)

        is_me = (sender == username)

        align = "e" if is_me else "w"
        bubble_bg = "#DCF8C6" if is_me else "white"

        row = tk.Frame(outer, bg="#e5ddd5")
        row.pack(anchor=align, padx=10)

        img = profiles.get(sender)

        if img and not is_me:
            tk.Label(row, image=img, bg="#e5ddd5").pack(side="left", padx=5)
            imgs.append(img)

        box = tk.Frame(row, bg="#e5ddd5")
        box.pack(side="left" if not is_me else "right")

        tk.Label(
            box,
            text=msg,
            bg=bubble_bg,
            fg="black",
            padx=10,
            pady=6,
            wraplength=350
        ).pack(anchor="w")

        if img and is_me:
            tk.Label(row, image=img, bg="#e5ddd5").pack(side="right", padx=5)
            imgs.append(img)

        canvas.update_idletasks()
        canvas.yview_moveto(1.0)

    entry = tk.Entry(root, font=("Arial", 12))
    entry.pack(fill="x", padx=10, pady=5)

    def send():
        msg = entry.get()
        if msg.strip():
            add(msg, username)
            client.send(encrypt(msg))
            entry.delete(0, tk.END)

    tk.Button(root, text="Send", command=send,
              bg="#128C7E", fg="white").pack()

    def receive():
        while True:
            try:
                msg = decrypt(client.recv(4096))

                if msg.startswith("TYPING:"):
                    continue

                sender = msg.split(" [")[0] if "[" in msg else msg.split(":")[0]

                root.after(0, lambda m=msg, s=sender: add(m, s))
                winsound.Beep(800, 150)

            except:
                break

    threading.Thread(target=receive, daemon=True).start()

    root.mainloop()


# ---------------- START ----------------
auth_screen()