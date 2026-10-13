import tkinter as tk
from tkinter import messagebox
root = tk.Tk()
root.title("Калькулятор")
root.geometry("340x260")
a = tk.Entry(root);a.pack(pady=8)
b = tk.Entry(root);b.pack(pady=8)
operation = tk.StringVar(value="+")
tk.OptionMenu(root, operation, "+", "-", "*", "/").pack()
result = tk.Label(root, text="Результат: —");result.pack(pady=12)
def calculate():
    try:
        x,y=float(a.get()),float(b.get())
        op=operation.get()
        if op=="/" and y==0:
            raise ZeroDivisionError
        value={"+":lambda:x+y,"-":lambda:x-y,"*":lambda:x*y,"/":lambda:x/y}[op]()
        result.config(text=f"Результат: {value:g}")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите два числа")
    except ZeroDivisionError:
        messagebox.showerror("Ошибка", "На ноль делить нельзя")
tk.Button(root, text="Вычислить", command=calculate).pack()
root.mainloop()
