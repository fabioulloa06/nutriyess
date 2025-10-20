import sqlite3

conn = sqlite3.connect('nutriyess.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tablas existentes:", tables)
conn.close()
