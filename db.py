from lib.SQL.DB import DB

db = DB.from_yaml('db_info.yml')
db.insert_table('INSERT INTO WeightRecords(record_date, weight) VALUES (DATE(\'2023-10-26\'), 3.4)')
table = db.fetch_table('SELECT * FROM WeightRecords')
print(table)
