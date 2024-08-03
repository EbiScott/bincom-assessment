import sqlite3

conn = sqlite3.connect('election.db')
cursor = conn.cursor()

with open('bincom_test.sql', 'r') as f:
    sql = f.read()

cursor.executescript(sql)
conn.commit()
conn.close()
