import sqlite3

def init_db():
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    
    # Products Table with ImageURL
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
        ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT, 
        Price REAL, 
        Category TEXT, 
        Stock INTEGER,
        ImageURL TEXT)''')

    # Orders Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
        OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
        ProductID INTEGER,
        CustomerName TEXT,
        Quantity INTEGER,
        TotalAmount REAL,
        OrderDate TEXT)''')

    conn.commit()
    conn.close()
    print("Store Database Initialized with Image Support.")

if __name__ == "__main__":
    init_db()