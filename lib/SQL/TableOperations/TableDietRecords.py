from lib.SQL.DB import DB
from lib.SQL.TableOperations.DBTableProtocol import DBTableProtocol


class TableDietRecords(DBTableProtocol):
    def __init__(self, db_instance: DB):
        super().__init__(db_instance)

    @property
    def TABLE_NAME(self):
        return 'DietRecords'

    @property
    def EDITABLE_COLUMNS(self):
        return ['food_id', 'food_quantity', 'diet_timestamp']

    @property
    def PRIMARY_KEY(self):
        return 'diet_id'

    @property
    def FOREIGN_KEYS(self):
        return ['food_id']

    def add_diet_record(self, food_id: int, quantity: float, timestamp: str = None):
        """

        :param food_id:
        :param quantity:
        :param timestamp: Only support format like '2023-10-27 10:34:07'
        :return:
        """
        insert_dict = {'food_id': food_id, 'food_quantity': quantity}
        if timestamp is not None:
            insert_dict.update({'diet_timestamp': timestamp})
        self.insert_record(insert_dict)

    def get_diet_records_all(self):
        return self.fetch_table()

    def get_diet_record_by_id(self, diet_id: int):
        return self.fetch_record(diet_id)

    def get_diet_record_by_timestamp(self, timestamp: str):
        command = f'''
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE diet_timestamp = TIMESTAMP(\'{timestamp}\')
        '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def get_diet_records_by_date(self, date: str):
        command = f'''
            SELECT * 
            FROM {self.TABLE_NAME}
            WHERE DATE(diet_timestamp) = DATE('{date}')
        '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def get_diet_records_by_interval(self, interval_start: str = None, interval_end: str = None):
        if (interval_start, interval_end) == (None, None):
            command = f'''
                SELECT * FROM {self.TABLE_NAME}
            '''
        elif interval_start is not None and interval_end is None:
            command = f'''
                SELECT * 
                FROM {self.TABLE_NAME}
                WHERE diet_timestamp >= TIMESTAMP('{interval_start}')
            '''
        elif interval_start is None and interval_end is not None:
            command = f'''
                SELECT * 
                FROM {self.TABLE_NAME}
                WHERE diet_timestamp <= TIMESTAMP('{interval_end}')
            '''
        else:
            command = f'''
                SELECT * 
                FROM {self.TABLE_NAME}
                WHERE diet_timestamp >= TIMESTAMP('{interval_start}')
                 AND diet_timestamp <= TIMESTAMP('{interval_end}')
            '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def delete_diet_record_by_id(self, diet_id: int):
        self.delete_record(diet_id)

    def update_diet_record_by_id_with_dict(self, diet_id: int, update_dict: dict):
        self.update_record(diet_id, update_dict)


def test():
    db = DB.from_yaml('../../../db_info.yml')
    table_diet = TableDietRecords(db)

    table_diet.add_diet_record(food_id=12, quantity=100, timestamp='2023-11-11 00:00:00')

    record = table_diet.get_diet_record_by_timestamp('2026-01-01 14:00:00')
    print(record)
    record = table_diet.get_diet_records_by_date('2023-10-22')
    print(record)
    record = table_diet.get_diet_records_by_interval(interval_start='2023-10-19', interval_end='2023-10-24 23:59:59')
    print(record)


if __name__ == '__main__':
    test()
