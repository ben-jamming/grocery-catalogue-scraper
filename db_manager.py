import sqlite3

# Connect to the database (this will create one if it doesn't exist)
conn = sqlite3.connect('grocery_items_db.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table as per requirement
sql = '''CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            price TEXT,
            product_id TEXT
         )'''
cursor.execute(sql)

# Commit your changes in the database
conn.commit()

# Close the connection
conn.close()
