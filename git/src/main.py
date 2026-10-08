import json
import os


class Order:
    TAX_RATE = 0.10  # 10% налог
    SERVICE_CHARGE = 0.05  # 5% сервисный сбор

    def __init__(self, customer):
        self.customer = customer
        self.dishes = []

    def add_dish(self, dish):
        if isinstance(dish, Dish):
            self.dishes.append(dish)
        else:
            raise ValueError("Можно добавлять только объекты класса Dish.")

    def calculate_total(self):
        return sum(dish.price for dish in self.dishes)

    def final_total(self):
        total = self.calculate_total()
        return total * (1 + Order.TAX_RATE) * (1 + Order.SERVICE_CHARGE)

    def __str__(self):
        dish_list = "\n".join([str(dish) for dish in self.dishes])
        return (
            f"Order for {self.customer.name}:\n"
            f"{dish_list}\n"
            f"Total: ${self.final_total():.2f}"
        )


class Dish:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return f"Dish: {self.name}, Category: {self.category}, Price: ${self.price:.2f}"


class Customer:
    def __init__(self, name, membership="Regular"):
        self.name = name
        self.membership = membership


def load_books(filename="library.json"):
    """Загрузка списка книг из JSON-файла."""
    if not os.path.isfile(filename):
        return []

    with open(filename, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def saving_books(books, filename="library.json"):
    """Сохранение списка книг в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(books, file, ensure_ascii=False, indent=4)


def list_books(books):
    """Возвращает строку со списком всех книг."""
    if not books:
        return "Библиотека пуста."

    result_lines = []

    for idx, book in enumerate(books, start=1):
        result_lines.append(
            f"{idx}. {book['title']} | {book['author']} | {book['year']}"
        )

    return "\n".join(result_lines)


def add_book(books, title, author, year):
    """Возвращает новый список с добавленной книгой."""
    new_book = {
        "title": title,
        "author": author,
        "year": year,
    }

    return books + [new_book]


def remove_book(books, title):
    """Возвращает новый список без книги с указанным названием."""
    return [book for book in books if book["title"].lower() != title.lower()]


def search_books(books, keyword):
    """Поиск книг по ключевому слову в названии и авторе."""
    keyword_lower = keyword.lower()

    return [
        book
        for book in books
        if keyword_lower in book["title"].lower()
        or keyword_lower in book["author"].lower()
    ]


def main():
    """Точка входа: меню управления библиотекой."""
    books = load_books()

    while True:
        print("\n=== Управление онлайн-библиотекой ===")
        print("1. Показать все книги")
        print("2. Добавить книгу")
        print("3. Удалить книгу")
        print("4. Поиск книг")
        print("5. Выйти")

        choice = input("Выберите действие (1-5): ").strip()

        if choice == "1":
            print("\nСписок книг:")
            print(list_books(books))

        elif choice == "2":
            title = input("Введите название: ").strip()
            author = input("Введите автора: ").strip()
            year = input("Введите год издания: ").strip()

            books = add_book(books, title, author, year)
            saving_books(books)

            print("Книга добавлена!")

        elif choice == "3":
            title_to_remove = input("Введите название книги для удаления: ").strip()

            new_books = remove_book(books, title_to_remove)

            if len(new_books) < len(books):
                books = new_books
                saving_books(books)
                print("Книга удалена!")
            else:
                print("Книга с таким названием не найдена.")

        elif choice == "4":
            keyword = input("Введите ключевое слово: ").strip()
            found = search_books(books, keyword)

            print(list_books(found) if found else "Ничего не найдено.")

        elif choice == "5":
            print("Выход из программы.")
            break

        else:
            print("Некорректный ввод. Попробуйте ещё раз.")


if __name__ == "__main__":
    main()
