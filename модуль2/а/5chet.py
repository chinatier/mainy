import tkinter as tk
root = tk.Tk()
root.title("Счётчик")
root.geometry("320x230")
count = tk.IntVar(value=0)
tk.Label(root, textvariable=count, font=("Arial", 40)).pack(pady=20)
tk.Button(root, text="Добавить", command=lambda: count.set(count.get() + 1)).pack(pady=5)
tk.Button(root, text="Сбросить", command=lambda: count.set(0)).pack(pady=5)
root.mainloop()
