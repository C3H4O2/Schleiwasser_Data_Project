from entry import Entry
import os

os.remove('data.db')

entry = Entry()
entry.setup_db()
