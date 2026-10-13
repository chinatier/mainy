import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import date, timedelta
from pathlib import Path

base = Path(__file__).parent
conn = sqlite3.connect(base / 'shop.db')
conn.execute('PRAGMA foreign_keys = ON')
conn.executescript((base / 'db.sql').read_text(encoding='utf-8'))

window = tk.Tk()
window.title('Чудо Обувь — Каталог')
window.geometry('850x650')
window.configure(bg='#f4f4f4')


def login():
    login_name = name.get().strip()
    if not login_name:
        messagebox.showwarning('Вход', 'Введите логин')
        return
    user = conn.execute('SELECT first_name FROM users WHERE login = ?', (login_name,)).fetchone()
    if not user:
        messagebox.showerror('Вход', 'Пользователь не найден')
        return
    login_frame.pack_forget()
    catalog_frame.pack(fill='both', expand=True)
    show_catalog()


def show_catalog():
    for widget in products_frame.winfo_children():
        widget.destroy()
    today = date.today().replace(day=1)
    last_month = (today - timedelta(days=1)).replace(day=1)
    rows = conn.execute('''
        SELECT p.id, p.name, p.category, p.manufacturer, p.composition,
               p.price, COALESCE(SUM(s.quantity_available), 0)
        FROM products p LEFT JOIN stock_items s ON s.product_id = p.id
        GROUP BY p.id
    ''').fetchall()
    for product_id, title, category, maker, composition, price, quantity in rows:
        ordered = conn.execute('''
            SELECT 1 FROM order_items i JOIN orders o ON o.id = i.order_id
            WHERE i.product_id = ? AND o.order_date >= ? AND o.order_date < ? LIMIT 1
        ''', (product_id, last_month.isoformat(), today.isoformat())).fetchone()
        actual_price = price if ordered else round(price * 0.75, 2)
        color = '#ffdada' if quantity <= 3 else '#ffffff'
        card = tk.Frame(products_frame, bg=color, bd=1, relief='solid')
        card.pack(fill='x', padx=12, pady=5)
        tk.Label(card, text=f'{maker} | {title}', bg=color, font=('Arial', 13, 'bold')).pack(anchor='w', padx=12, pady=3)
        tk.Label(card, text=f'{category}    Состав: {composition}    В наличии: {quantity}    Цена: {actual_price:.2f} ₽', bg=color).pack(anchor='w', padx=12, pady=5)


login_frame = tk.Frame(window, bg='#f4f4f4')
login_frame.pack(pady=100)
tk.Label(login_frame, text='Чудо Обувь', font=('Arial', 24, 'bold'), bg='#f4f4f4').pack(pady=15)
tk.Label(login_frame, text='Логин', bg='#f4f4f4').pack()
name = tk.Entry(login_frame, font=('Arial', 14))
name.pack(pady=10)
tk.Button(login_frame, text='Войти', command=login).pack(pady=10)

catalog_frame = tk.Frame(window, bg='#f4f4f4')
tk.Label(catalog_frame, text='Каталог обуви', font=('Arial', 22, 'bold'), bg='#f4f4f4').pack(pady=15)
products_frame = tk.Frame(catalog_frame, bg='#f4f4f4')
products_frame.pack(fill='both', expand=True)

window.mainloop()
conn.close()
