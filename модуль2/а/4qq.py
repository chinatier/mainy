import tkinter as tk
root = tk.Tk()
root.title("Приветствие")
root.geometry("360x220")
tk.Label(root, text="Как вас зовут?").pack(pady=12)
name = tk.Entry(root, font=("Arial", 13))
name.pack()
result = tk.Label(root, text="")
result.pack(pady=14)
def greet():
    value = name.get().strip()
    result.config(text=f"Привет, {value}!" if value else "Введите имя")
tk.Button(root, text="Поздороваться", command=greet).pack()
root.mainloop()
