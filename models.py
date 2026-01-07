import sqlite3

class Product:
    def __init__(self, name, price, category, stock, image="placeholder.jpg", p_id=None):
        self.id = p_id
        self.name = name
        self.price = float(price)
        self.category = category
        self.stock = int(stock)
        self.image = image

    def save(self):
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Products (Name, Price, Category, Stock, ImageURL) VALUES (?, ?, ?, ?, ?)", 
                       (self.name, self.price, self.category, self.stock, self.image))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ProductID, Name, Price, Category, Stock, ImageURL FROM Products ORDER BY ProductID DESC")
        rows = cursor.fetchall()
        conn.close()
        return [Product(r[1], r[2], r[3], r[4], r[5], r[0]) for r in rows]

    @staticmethod
    def get_by_id(p_id):
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ProductID, Name, Price, Category, Stock, ImageURL FROM Products WHERE ProductID = ?", (p_id,))
        r = cursor.fetchone()
        conn.close()
        return Product(r[1], r[2], r[3], r[4], r[5], r[0]) if r else None