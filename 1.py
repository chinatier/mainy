import tkinter as tk

window = tk.Tk()
window.title("моя визитка")
window.geometry("350x250")

label = tk.Label(window, text="privet mir!", font=("Arial", 20))
label.pack(pady=20)
label = tk.Label(window, text="студент", font=("Arial", 20))
label.pack(pady=10)
label = tk.Label(window, text="ГОРОД", font=("Arial", 20))
label.pack(pady=10)
window.mainloop()