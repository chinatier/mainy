import tkinter as tk

window = tk.Tk()
window.title("RANDOM")
window.geometry("1920x1080")

def login():
    if name.get():
        login_frame.pack_forget()
        catalog_frame.pack(pady=50)


login_frame = tk.Frame(window)
login_frame.pack(pady=100)
tk.Label(login_frame, text="Логин", font=("Arial Bold", 20)).pack(pady=20)

name = tk.Entry(login_frame, text="Логин", font=("Arial Bold", 16))
name.pack(pady=10)

tk.Button (login_frame,text="Войти", command=login).pack(pady=10)

catalog_frame = tk.Frame(window)
tk.Label(catalog_frame, text="Каталог", font=("Arial Bold", 24)).pack(pady=20)


products(

window.mainloop()