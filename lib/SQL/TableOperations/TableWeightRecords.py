from lib.SQL.DB import DB
from lib.SQL.TableOperations.DBTableProtocol import DBTableProtocol


class TableWeightRecords(DBTableProtocol):
    def __init__(self, db_instance: DB):
        super().__init__(db_instance)

    @property
    def TABLE_NAME(self):
        return 'WeightRecords'

    @property
    def EDITABLE_COLUMNS(self):
        return ['record_date', 'weight']

    @property
    def PRIMARY_KEY(self):
        return 'record_date'

    @property
    def FOREIGN_KEYS(self):
        return []

    def insert_record(self, insert_dict: dict):
        assert all((key in self.EDITABLE_COLUMNS) for key in list(
            insert_dict.keys())), 'Find unsupported keys, only [record_date, weight] are supported'

        self.db_instance.insert_row_to_table_by_dict(self.TABLE_NAME, insert_dict)

    def fetch_record(self, for_key: str):
        command = f'''
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE record_date = DATE(\'{for_key}\')
        '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def add_weight_record(self, weight: float, date: str = None):
        """

        :param weight:
        :param date: Only support format like '2023-10-27'
        :return:
        """
        if date is None:
            self.insert_record({'weight': weight})
        else:
            self.insert_record(
                {'record_date': f'DATE(\'{date}\')', 'weight': weight})

    def get_weight_records_all(self):
        command = f'''
            SELECT * 
            FROM {self.TABLE_NAME}
        '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def get_weight_record_by_date(self, date: str):
        return self.fetch_record(date)

    def get_weight_records_by_interval(self, interval_start: str = None, interval_end: str = None):
        if (interval_start, interval_end) == (None, None):
            command = f'''
                SELECT * FROM {self.TABLE_NAME}
            '''
        elif interval_start is not None and interval_end is None:
            command = f'''
                SELECT * 
                FROM {self.TABLE_NAME}
                WHERE record_date >= DATE('{interval_start}')
            '''
        elif interval_start is None and interval_end is not None:
            command = f'''
                SELECT * 
                FROM {self.TABLE_NAME}
                WHERE record_date <= DATE('{interval_end}')
            '''
        else:
            command = f'''
                SELECT * 
                FROM {self.TABLE_NAME}
                WHERE record_date >= DATE('{interval_start}')
                 AND record_date <= DATE('{interval_end}')
            '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def delete_weight_record_by_date(self, date: str):
        self.delete_record(date)

    def update_weight_record_by_date_with_dict(self, date: str, update_dict: dict):
        self.update_record(date, update_dict)


def test():
    db = DB.from_yaml('../../../db_info.yml')
    table_weight = TableWeightRecords(db)

    table_weight.add_weight_record(3.7, '2036-01-02')

    result = table_weight.fetch_record('2023-10-20')
    print(result)
    result = table_weight.get_weight_records_by_interval(interval_start='2023-10-20')
    print(result)


if __name__ == '__main__':
    test()
