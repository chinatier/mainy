import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import psycopg2


def get_products():
    conn = psycopg2.connect(host=os.getenv("DB_HOST", "localhost"), database=os.getenv("DB_NAME", "Proba"), user=os.getenv("DB_USER", "postgres"),
                            password=os.getenv("DB_PASSWORD", ""), port=os.getenv("DB_PORT", "5432"))
    cur = conn.cursor()
    cur.execute("""
        SELECT p.manufacturer, p.product_name, p.category,
               COALESCE(SUM(s.quantity_available), 0), p.composition, p.price
        FROM products p
        LEFT JOIN stock_items s ON s.product_id = p.product_id
        GROUP BY p.product_id
        ORDER BY p.product_id;
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_user_fio(login):
    conn = psycopg2.connect(host=os.getenv("DB_HOST", "localhost"), database=os.getenv("DB_NAME", "Proba"), user=os.getenv("DB_USER", "postgres"),
                            password=os.getenv("DB_PASSWORD", ""), port=os.getenv("DB_PORT", "5432"))
    cur = conn.cursor()
    cur.execute("SELECT last_name, first_name, middle_name FROM users WHERE login = %s;", (login,))
    row = cur.fetchone()
    conn.close()
    if row:
        return f"{row[0]} {row[1]} {row[2] or ''}".strip()
    return None


def login():
    try:
        fio = get_user_fio(entry_login.get().strip())
    except psycopg2.Error as exc:
        messagebox.showerror("Ошибка подключения", str(exc))
        return
    if fio:
        messagebox.showinfo("Вход", f"Добро пожаловать, {fio}!")
        window.withdraw()
        main(fio)
    else:
        messagebox.showerror("Ошибка", "Пользователь не найден")


def main(user_fio):
    win2 = tk.Toplevel(window)
    win2.title("Главное меню")
    win2.geometry("600x250")
    win2.protocol("WM_DELETE_WINDOW", window.destroy)

    def go_katalog():
        win2.destroy()
        katalog(user_fio)

    def go_kozina():
        win2.destroy()
        kozina(user_fio)

    def logout():
        win2.destroy()
        entry_login.delete(0, tk.END)
        window.deiconify()

    tk.Label(win2, text="МАГАЗИН ОБУВИ", font=("Arial", 16)).pack(pady=10)

    bar = tk.Frame(win2, bg="lightgray")
    bar.pack(fill="x")

    tk.Button(bar, text="Каталог", command=go_katalog).pack(side="left", padx=5, pady=5)
    tk.Button(bar, text="Корзина", command=go_kozina).pack(side="left", padx=5, pady=5)
    tk.Label(bar, text=user_fio, bg="lightgray").pack(side="right", padx=5)
    tk.Button(bar, text="Выйти", command=logout).pack(side="right", padx=5, pady=5)


def katalog(user_fio):
    win3 = tk.Toplevel(window)
    win3.title("Каталог")
    win3.geometry("750x550")
    win3.protocol("WM_DELETE_WINDOW", window.destroy)

    def go_back():
        win3.destroy()
        main(user_fio)

    tk.Label(win3, text=user_fio).pack(anchor="ne", padx=10)
    tk.Label(win3, text="КАТАЛОГ", font=("Arial", 16)).pack(pady=10)
    tk.Button(win3, text="Назад", command=go_back).pack()

    canvas = tk.Canvas(win3)
    scroll = tk.Scrollbar(win3, command=canvas.yview)
    canvas.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    cards = tk.Frame(canvas)
    canvas.create_window((0, 0), window=cards, anchor="nw")
    cards.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    img = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "picture.png")).resize((120, 80))
    photo = ImageTk.PhotoImage(img)
    win3.photo = photo

    try:
        products = get_products()
    except psycopg2.Error as exc:
        messagebox.showerror("Ошибка базы данных", str(exc))
        return

    for manufacturer, name, category, qty, composition, price in products:
        card = tk.Frame(cards, bd=1, relief="solid")
        card.pack(fill="x", padx=10, pady=5)

        tk.Label(card, image=photo).pack(side="left", padx=10, pady=10)
        tk.Label(card, text=f"{price} ₽", font=("Arial", 16)).pack(side="right", padx=20)

        info = tk.Frame(card)
        info.pack(side="left")
        tk.Label(info, text=f"{manufacturer} | {name}", font=("Arial", 11, "bold"),
                 wraplength=350, justify="left").pack(anchor="w")
        tk.Label(info, text=f"Категория: {category}").pack(anchor="w")
        tk.Label(info, text=f"Количество: {qty}").pack(anchor="w")
        tk.Label(info, text=f"Состав: {composition}", font=("Arial", 8),
                 wraplength=350, justify="left").pack(anchor="w")


def kozina(user_fio):
    win4 = tk.Toplevel(window)
    win4.title("Корзина")
    win4.geometry("400x250")
    win4.protocol("WM_DELETE_WINDOW", window.destroy)

    def go_back():
        win4.destroy()
        main(user_fio)

    tk.Label(win4, text=user_fio).pack(anchor="ne", padx=10)
    tk.Label(win4, text="КОРЗИНА", font=("Arial", 16)).pack(pady=10)
    tk.Button(win4, text="Назад", command=go_back).pack()


window = tk.Tk()
window.title("Магазин обуви")
window.geometry("300x200")

tk.Label(window, text="Логин").pack()
entry_login = tk.Entry(window)
entry_login.pack()

tk.Button(window, text="Войти", command=login).pack(pady=20)

window.mainloop()
