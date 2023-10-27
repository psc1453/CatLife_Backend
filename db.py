from lib.SQL.DB import DB

db = DB.from_yaml('db_info.yml')
db.insert_table_by_command('INSERT INTO WeightRecords(record_date, weight) VALUES (DATE(\'2023-11-01\'), 3.4)')
db.insert_table_by_dict('WeightRecords', {'record_date': 'DATE(\'2023-11-02\')', 'weight': '3.9'})
table = db.fetch_table_by_command('SELECT * FROM WeightRecords')
print(table)
