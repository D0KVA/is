import sqlite3

class Apteka:
    def __init__(self, db_name='IS.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Lekarstva (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        self.conn.commit()

        self.cursor.execute('DELETE FROM Lekarstva')
        self.conn.commit()

        self.cursor.executemany('INSERT INTO Lekarstva (name, price) VALUES (?, ?)', [
            ('Ибупрофен', 120),
            ('Парацетамол', 80),
            ('Ибупранол', 50),
            ('Панасонисон', 150),
            ('Бебриниум', 250),
        ])
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shopping_cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        ''')
        self.conn.commit()

    def close_connection(self):
        self.conn.close()