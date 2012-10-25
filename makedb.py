#!/usr/bin/python
import sqlite3

dbconn = sqlite3.connect('./tweets.db')
dbconn.execute('''create table tweetz (tweet_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet TEXT,sname TEXT,timestamp TEXT,category TEXT,linkz TEXT)''')
dbconn.commit()
dbconn.close()
