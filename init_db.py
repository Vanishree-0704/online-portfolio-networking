import sqlite3

conn = sqlite3.connect("portfolio.db")
cursor = conn.cursor()

# Contact messages table
cursor.execute("""
CREATE TABLE IF NOT EXISTS contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    subject TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Admin users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

# Default admin user
cursor.execute("""
INSERT INTO admin_users (username, password)
VALUES ('admin', 'admin123')
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully")
