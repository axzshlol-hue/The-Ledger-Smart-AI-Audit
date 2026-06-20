import sqlite3

def init_db():
    conn = sqlite3.connect('ledger.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results 
                 (student_id TEXT PRIMARY KEY, score INTEGER, report TEXT)''')
    conn.commit()
    conn.close()

def save_audit(student_id, score, report):
    conn = sqlite3.connect('ledger.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO results VALUES (?, ?, ?)", (student_id, score, report))
    conn.commit()
    conn.close()