import sqlite3

# Create a connection to the SQLite database (if it doesn't exist, it will be created)
conn = sqlite3.connect('library.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create tables for books and categories
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

# Sample data to insert into tables
sample_categories = [
    ('Category 1',),
    ('Category 2',),
    # Add more categories as needed
]

sample_books = [
    ('Book 1', 'Author 1', 1),
    ('Book 2', 'Author 2', 2),
    # Add more books as needed
]

# Insert sample data into categories table
cursor.executemany('INSERT INTO categories (name) VALUES (?)', sample_categories)

# Insert sample data into books table
cursor.executemany('INSERT INTO books (title, author, category_id) VALUES (?, ?, ?)', sample_books)

# Commit changes and close the connection
conn.commit()
conn.close()
