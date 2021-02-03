import database_helper

con = database_helper.db_connect()
cur = con.cursor()

sample_id = database_helper.create_sample(con,1,2021,'5577','http://sirius.bu.edu/data/')



# cur.execute("SELECT id, place FROM places")
# results = cur.fetchall()
# for row in results:
#     print(row)

