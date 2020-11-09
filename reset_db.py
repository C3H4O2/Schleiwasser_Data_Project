from entry import Entry
import os

try:
    os.remove('data.db')
except:
    pass

entry = Entry()
entry.setup_db()
