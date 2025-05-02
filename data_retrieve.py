import sqlite3
conn = sqlite3.connect('farmer.db')
query = "select * from farmerdata"

cur_obj = conn.cursor()
cur_obj.execute(query)

for record in cur_obj.fetchall():
    print(record)

cur_obj.close()
conn.close()