from apteka import Apteka
from users import Client, Administrator

ap = Apteka()

while True:
    print("Чтобы войти в Аптеку, вам необходимо авторизоваться или зарегистрироваться")

    print("1. Авторизоваться")
    print("2. Зарегистрироваться")
    print("3. Выйти")
    a = input("\nВыберите действие: ")

    if a == '1':
        print("Авторизация")
        print("1. Авторизоваться как клиент")
        print("2. Авторизоваться как сотрудник")
        print("3. Вернуться назад")
        c = input("\nВыберите действие: ")

        if c == '1':
            client = Client(ap)

            while True:
                login = input("Введите логин: ")
                passw = input("Введите пароль: ")

                if login.strip() and passw.strip():
                    break
                else:
                    print("Логин и пароль не должны быть пустыми.")

            if client.authenticate(login, passw):
                print("Вы авторизовались")
            else:
                continue

            while True:
                print("Добро пожаловать в Аптеку.")
                print("1. Товары")
                print("2. Корзина")
                print("3. Выйти")

                client_action = input("Выберите действие: ")

                if client_action == '1':
                    client.display_products()

                elif client_action == '2':
                    client.display_cart()

                    print("1. Оформить заказ")
                    print("2. Вернуться назад")
                    cart_choice = input("Выберите действие: ")

                    if cart_choice == '1':
                        print("Оформление заказа")

                        address = input("Введите адрес доставки: ")
                        client.checkout(address)
                        break

                    elif cart_choice == '2':
                        continue

                elif client_action == '3':
                    print("До свидания.")
                    break

        elif c == '2':
            admin = Administrator(ap)

            while True:
                admin_login = input("Введите логин: ")
                admin_password = input("Введите пароль: ")

                if admin_login.strip() and admin_password.strip():
                    break
                else:
                    print("У вас что-то пустое")

            if admin.authenticate(admin_login, admin_password):
                print("\nАвторизация прошла успешно!")

                while True:
                    print("Что бы вы хотели изменить в Аптеке?")
                    print("1. Добавить товар")
                    print("2. Удалить товар")
                    print("3. Изменить название товара")
                    print("4. Выйти")

                    b = input("\nВыберите действие: ")

                    if b == '1':
                        print("Добавление товара")
                        while True:
                            product_name = input("\nВведите название товара: ")
                            product_price = input("Введите цену товара: ")
                            try:
                                product_price = float(product_price)
                                if product_name.strip() and product_price >= 0:
                                    admin.add_product(product_name, product_price)
                                    print(f"Товар '{product_name}' успешно добавлен.")
                                    break
                                else:
                                    print("Название товара или цена неверно")
                            except ValueError:
                                print("Неверная цена")

                    elif b == '2':
                        print("Удаление товара")
                        while True:
                            product_name_to_delete = input("\nВведите название товара для удаления (или '0' для возвращения назад): ")

                            if product_name_to_delete == '0':
                                break

                            admin.remove_product(product_name_to_delete)
                            print(f"Товар '{product_name_to_delete}' успешно удален.")
                            break

                    elif b == '3':
                        print("Изменение товара")
                        while True:
                            product_name_to_change = input("\nВведите название товара для изменения (или '0' для возвращения назад): ")

                            if product_name_to_change == '0':
                                break

                            new_product_name = input("Введите новое название товара: ")
                            admin.change_product_name(product_name_to_change, new_product_name)
                            print(f"Название товара успешно изменено на '{new_product_name}'.")
                            break

                    elif b == '4':
                        print("Вы вышли.")
                        break
            else:
                print("Неправильный логин или пароль. Пожалуйста, попробуйте снова.")

    elif a == '2':
        print("Регистрация")
        print("Логин должен быть не менее 4 символов")

        while True:
            login = input("\nПридумайте логин: ")

            if len(login) >= 4:
                break
            else:
                print("Логин должен содержать не менее 4 символов и не должен быть пустым. Пожалуйста, попробуйте снова.")

        while True:
            passw = input("Придумайте пароль: ")

            if len(passw) > 0:
                break
            else:
                print("Пароль не должен быть пустым..")

        ap.cursor.execute('SELECT * FROM users WHERE login = ?', (login,))
        existing_user = ap.cursor.fetchone()

        if existing_user:
            print("Такой чел уже есть.")

    elif a == '3':
        print("Вы вышли")
        break

    else:
        print("Неправильный ввод. Пожалуйста, попробуйте снова.")

ap.close_connection()