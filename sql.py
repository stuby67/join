import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('sales.db')
cursor = conn.cursor()

# Create customers table
cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY,
                    customer_name TEXT,
                    customer_email TEXT
                )''')

# Create products table
cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY,
                    product_name TEXT,
                    product_price REAL
                )''')

# Create sales table
cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                    sale_id INTEGER PRIMARY KEY,
                    customer_id INTEGER,
                    product_id INTEGER,
                    sale_date TEXT,
                    quantity INTEGER,
                    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
                    FOREIGN KEY (product_id) REFERENCES products (product_id)
                )''')

# Sample data for customers table
customers_data = [
    (1, 'John Smith', 'john@example.com'),
    (2, 'Jane Doe', 'jane@example.com')
]

# Sample data for products table
products_data = [
    (101, 'Laptop', 1000),
    (102, 'Smartphone', 500)
]


sales_data = [
    (1, 1, 101, '2024-06-01', 2),
    (2, 2, 102, '2024-06-02', 1),
    (3, 1, 102, '2024-06-03', 1)
]

# Insert sample data into customers table
cursor.executemany('INSERT INTO customers VALUES (?, ?, ?)', customers_data)

# Insert sample data into products table
cursor.executemany('INSERT INTO products VALUES (?, ?, ?)', products_data)

# Insert sample data into sales table
cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', sales_data)

# Commit changes and close connection
conn.commit()
conn.close()

print("Tables created and sample data inserted successfully.")
