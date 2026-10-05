import tkinter as tk

window = tk.Tk()
window.title("Счетчик кликов")
window.geometry("300x250")

count = 0

def on_click():
    global count
    count += 1
    label.config(text=count)
def reset():
    global cunt
    count = 0
    label.config(text=count)

label = tk.Label(window, text="0")
label.pack(pady=30)
button = tk.Button(window, text="Клик!", command=on_click)
button.pack(pady=10)
reset_button = tk.Button(window, text="Сброс", command=reset)
reset_button.pack()
window.mainloop() 