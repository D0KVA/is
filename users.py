import random

class User:
    def __init__(self, Apteka):
        self.Apteka = Apteka
        self.authenticated_user = None

    def validate_credentials(self, login, password):
        if not login.strip() or not password.strip():
            print("Логин и пароль не могут быть пустыми. Пожалуйста, попробуйте снова.")
            return False
        return True

    def authenticate(self, login, password):
        if not self.validate_credentials(login, password):
            return False

        self.Apteka.cursor.execute('SELECT * FROM users WHERE login = ?', (login,))
        existing_user = self.Apteka.cursor.fetchone()

    def display_products(self):
        self.Apteka.cursor.execute('SELECT * FROM products')
        products = self.Apteka.cursor.fetchall()
        print("Товары в Аптеке")
        for product in products:
            print(f"{product[0]}. {product[1]} - ${product[2]}")
        return products

class Client(User):
    def __init__(self, Apteka):
        super().__init__(Apteka)

    def validate_product_id(self, product_id, products):
        try:
            product_id = int(product_id)
            if not (1 <= product_id <= len(products)):
                print("Неверный номер товара. Пожалуйста, попробуйте снова.")
                return False
            return True
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите число.")
            return False

    def add_to_cart(self, product_id):
        products = self.display_products()
        if not self.validate_product_id(product_id, products):
            return

        self.Apteka.cursor.execute('INSERT INTO shopping_cart (user_id, product_id) VALUES (?, ?)',
        (self.authenticated_user[0], product_id))
        self.Apteka.conn.commit()

class Administrator(User):
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin"

    def authenticate(self, login, password):
        return login == self.ADMIN_USERNAME and password == self.ADMIN_PASSWORD

    def add_product(self, name, price):
        self.Apteka.cursor.execute('INSERT INTO Lekarstva (name, price) VALUES (?, ?)', (name, price))
        self.Apteka.conn.commit()

    def remove_product(self, name):
        self.Apteka.cursor.execute('DELETE FROM Lekarstva WHERE name = ?', (name))
        self.Apteka.conn.commit()

    def change_product_name(self, current_name, new_name):
        self.store.cursor.execute('UPDATE Lekarstva SET name = ? WHERE name = ?', (new_name, current_name))
        self.store.conn.commit()
