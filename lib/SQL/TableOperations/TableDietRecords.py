from lib.SQL.DB import DB
from lib.SQL.TableOperations.DBTableProtocol import DBTableProtocol


class TableDietRecords(DBTableProtocol):
    def __init__(self, db_instance: DB):
        super().__init__(db_instance)

    @property
    def table_name(self):
        return 'DietRecords'

    def insert_record(self, insert_dict: dict):
        assert all((key in ['food_id', 'food_quantity', 'diet_timestamp']) for key in list(
            insert_dict.keys())), \
            'Find unsupported keys, only [food_id, food_quantity, diet_timestamp] are supported'

        self.db_instance.insert_table_by_dict(self.table_name, insert_dict)

    def fetch_record(self, for_key: int):
        command = '''
            SELECT *
            FROM {table_name}
            WHERE food_id = {id}
        '''.format(table_name=self.table_name, id=for_key)
        table = self.db_instance.fetch_table_by_command(command)
        return table

    # TODO: Add the delete and update functions.
    def delete_record(self, for_key: int):
        pass

    def update_record(self, for_key: int, new_dict: dict):
        pass

    def add_diet_record(self, food_id: int, quantity: float, timestamp: str = None):
        """

        :param food_id:
        :param food_quantity:
        :param diet_timestamp: Only support format like '2023-10-27 10:34:07'
        :return:
        """
        insert_dict = {'food_id': food_id, 'food_quantity': quantity}
        if timestamp is not None:
            insert_dict.update({'diet_timestamp': timestamp})
        self.insert_record(insert_dict)

    def get_diet_records_by_timestamp(self, timestamp: str):
        command = '''
                    SELECT *
                    FROM {table_name}
                    WHERE diet_timestamp = TIMESTAMP(\'{timestamp}\')
                '''.format(table_name=self.table_name, timestamp=timestamp)
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def get_diet_records_by_date(self, date: str):
        command = '''
            SELECT * 
            FROM {table_name}
            WHERE DATE(diet_timestamp) = DATE('{date}')
        '''.format(table_name=self.table_name, date=date)
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def get_diet_records_by_interval(self, interval_start: str = None, interval_end: str = None):
        if (interval_start, interval_end) == (None, None):
            command = '''
                SELECT * FROM {table_name}
            '''.format(table_name=self.table_name)
        elif interval_start is not None and interval_end is None:
            command = '''
                SELECT * 
                FROM {table_name}
                WHERE diet_timestamp >= TIMESTAMP('{timestamp_start}')
            '''.format(table_name=self.table_name, timestamp_start=interval_start)
        elif interval_start is None and interval_end is not None:
            command = '''
                SELECT * 
                FROM {table_name}
                WHERE diet_timestamp <= TIMESTAMP('{timestamp_end}')
            '''.format(table_name=self.table_name, timestamp_end=interval_end)
        else:
            command = '''
                SELECT * 
                FROM {table_name}
                WHERE diet_timestamp >= TIMESTAMP('{timestamp_start}')
                 AND diet_timestamp <= TIMESTAMP('{timestamp_end}')
            '''.format(table_name=self.table_name, timestamp_start=interval_start, timestamp_end=interval_end)
        table = self.db_instance.fetch_table_by_command(command)
        return table


def test():
    db = DB.from_yaml('../../../db_info.yml')
    table_diet = TableDietRecords(db)

    table_diet.add_diet_record(food_id=12, quantity=100, timestamp='2023-11-11 00:00:00')

    record = table_diet.get_diet_records_by_timestamp('2026-01-01 14:00:00')
    print(record)
    record = table_diet.get_diet_records_by_date('2023-10-22')
    print(record)
    record = table_diet.get_diet_records_by_interval(interval_start='2023-10-19', interval_end='2023-10-24 23:59:59')
    print(record)


if __name__ == '__main__':
    test()
