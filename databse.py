import sqlite3
conn = sqlite3.connect('farmer.db')

query = "create table farmerdata (N int, P int, h int, k int, ph int, r int, t int, prediction int)"
# N, P, h, k, ph, r, t, prediction

curs_obj = conn.cursor()

curs_obj.execute(query)
print("successfully created database and a table.")
conn.commit()
curs_obj.close()
conn.close()

