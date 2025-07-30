import customtkinter as ctk

from main import start_game

#from ag import run_game

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x300")
app.title("Лаунчер гри")

def run_game():
    name = name_entry.get()
    host = host_entry.get()
    port = port_entry.get()
    if name and host and port:
        app.destroy()
        start_game(name, host, port)


ctk.CTkLabel(app, text="Ім'я гравця:").pack(pady=10)
name_entry = ctk.CTkEntry(app)
name_entry.pack()

ctk.CTkLabel(app, text="Адреса сервера:").pack(pady=10)
host_entry = ctk.CTkEntry(app)
host_entry.insert(0, "2.tcp.eu.ngrok.io")
host_entry.pack()

ctk.CTkLabel(app, text="Порт:").pack(pady=10)
port_entry = ctk.CTkEntry(app)
port_entry.insert(0, "18875")
port_entry.pack()

ctk.CTkButton(app, text="Запустити гру", command=run_game).pack(pady=20)
error_label = ctk.CTkLabel(app, text="", text_color="red")
error_label.pack()

app.mainloop()
