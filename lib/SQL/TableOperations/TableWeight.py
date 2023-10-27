from lib.SQL.DB import DB
from lib.SQL.TableOperations.DBTableProtocol import DBTableProtocol


class TableWeight(DBTableProtocol):
    def __init__(self, db_instance: DB):
        super().__init__(db_instance)

    @property
    def table_name(self):
        return 'WeightRecords'

    def insert_record(self, insert_dict: dict):
        assert all((key in ['record_date', 'weight']) for key in list(
            insert_dict.keys())), 'Find unsupported keys, only [record_date, weight] are supported'

        self.db_instance.insert_table_by_dict(self.table_name, insert_dict)

    def fetch_record(self, for_key: str):
        command = '''
            SELECT *
            FROM {table_name}
            WHERE record_date = DATE(\'{date}\')
        '''.format(table_name=self.table_name, date=for_key).strip()
        print(command)
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def delete_record(self, for_key: str):
        pass

    def update_record(self, for_key: str, new_dict: dict):
        pass

    def add_weight_record(self, weight: float, date: str = None):
        """

        :param weight:
        :param date: Only support format like '2023-10-27'
        :return:
        """
        if date is None:
            self.insert_record({'weight': '{weight}'.format(weight=weight)})
        else:
            self.insert_record(
                {'record_date': 'DATE(\'{date}\')'.format(date=date), 'weight': '{weight}'.format(weight=weight)})

    def get_weight_records(self, interval_start: str = None, interval_end: str = None):
        if (interval_start, interval_end) == (None, None):
            command = '''
                SELECT * FROM {table_name}
            '''.format(table_name=self.table_name).strip()
        elif interval_start is not None and interval_end is None:
            command = '''
                SELECT * 
                FROM {table_name}
                WHERE record_date >= DATE('{date_start}')
            '''.format(table_name=self.table_name, date_start=interval_start).strip()
        elif interval_start is None and interval_end is not None:
            command = '''
                SELECT * 
                FROM {table_name}
                WHERE record_date <= DATE('{date_end}')
            '''.format(table_name=self.table_name, date_end=interval_end).strip()
        else:
            command = '''
                SELECT * 
                FROM {table_name}
                WHERE record_date >= DATE('{date_start}')
                 AND record_date <= DATE('{date_end}')
            '''.format(table_name=self.table_name, date_start=interval_start, date_end=interval_end).strip()
        print(command)
        table = self.db_instance.fetch_table_by_command(command)
        return table
