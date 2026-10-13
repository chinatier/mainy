def km_to_miles(km):
    return km * 0.621371

def kg_to_pounds(kg):
    return kg * 2.20462

if __name__ == "__main__":
    choice = input("1 — километры в мили, 2 — кг в фунты: ").strip()
    try:
        value = float(input("Введите значение: "))
        if choice == "1":
            print(f"{km_to_miles(value):.2f} миль")
        elif choice == "2":
            print(f"{kg_to_pounds(value):.2f} фунтов")
        else:
            print("Неизвестная операция")
    except ValueError:
        print("Введите число")
