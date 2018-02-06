# https://docs.python.org/2/library/sqlite3.html

import sqlite3
from string import printable
import random
import time
conn = sqlite3.connect('example.db')
c = conn.cursor()
try:
    c.execute('''CREATE TABLE logs
             (date text, body text)''')
except sqlite3.OperationalError:  # table already exists
    pass

if __name__ == '__main__':
    c.execute(
        "INSERT INTO logs VALUES (?,?)",
        (time.time(), ''.join([random.choice(printable) for i in range(30)])))
    conn.commit()
    results = c.execute('SELECT * FROM logs')
    for r in results:
        print(r)
