from enum import Enum
from typing import Union

from lib.SQL.DB import DB
from lib.SQL.TableOperations.DBTableProtocol import DBTableProtocol


class UrineStatus(Enum):
    normal = 0
    abnormal = 1


class TableUrineRecords(DBTableProtocol):
    def __init__(self, db_instance: DB):
        super().__init__(db_instance)

    @property
    def table_name(self):
        return 'UrineRecords'

    def insert_record(self, insert_dict: dict):
        assert all((key in ['urine_timestamp', 'urine_status', 'urine_comment']) for key in list(
            insert_dict.keys())), \
            'Find unsupported keys, only [urine_timestamp, urine_status, urine_comment] are supported'

        self.db_instance.insert_table_by_dict(self.table_name, insert_dict)

    def fetch_record(self, for_key: int):
        command = '''
            SELECT *
            FROM {table_name}
            WHERE urine_id = {id}
        '''.format(table_name=self.table_name, id=for_key).strip()
        table = self.db_instance.fetch_table_by_command(command)
        return table

    # TODO: Add the delete and update functions.
    def delete_record(self, for_key: int):
        pass

    def update_record(self, for_key: int, new_dict: dict):
        pass

    def add_urine_record(self, timestamp: str = None, status: Union[UrineStatus, str] = UrineStatus.normal,
                         comment: str = None):
        """

        :param timestamp: Only support format like '2023-10-27 10:34:07'
        :param status: Enum(UrineStatus.normal, UrineStatus.abnormal)
        :param comment:
        :return:
        """
        status_str = status if type(status) == str else status.name
        assert status_str in [s.name for s in UrineStatus], \
            ('Not a valid option for parameter \'status\'! '
             'Only [normal, abnormal] are support, or using UrineStatus which is more recommended!')
        insert_dict = {'urine_status': status_str}
        if timestamp is not None:
            insert_dict.update({'urine_timestamp': timestamp})
        if comment is not None:
            insert_dict.update({'urine_comment': comment})
        self.insert_record(insert_dict)

    def get_urine_records_by_timestamp(self, timestamp: str):
        command = '''
                    SELECT *
                    FROM {table_name}
                    WHERE urine_timestamp = TIMESTAMP(\'{timestamp}\')
        '''.format(table_name=self.table_name, timestamp=timestamp).strip()
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def get_urine_records_by_date(self, date: str):
        command = '''
            SELECT * 
            FROM {table_name}
            WHERE DATE(urine_timestamp) = DATE('{date}')
        '''.format(table_name=self.table_name, date=date).strip()
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def get_urine_records_by_interval(self, interval_start: str = None, interval_end: str = None):
        if (interval_start, interval_end) == (None, None):
            command = '''
                SELECT * FROM {table_name}
            '''.format(table_name=self.table_name).strip()
        elif interval_start is not None and interval_end is None:
            command = '''
                SELECT * 
                FROM {table_name}
                WHERE urine_timestamp >= TIMESTAMP('{timestamp_start}')
            '''.format(table_name=self.table_name, timestamp_start=interval_start).strip()
        elif interval_start is None and interval_end is not None:
            command = '''
                SELECT * 
                FROM {table_name}
                WHERE urine_timestamp <= TIMESTAMP('{timestamp_end}')
            '''.format(table_name=self.table_name, timestamp_end=interval_end).strip()
        else:
            command = '''
                SELECT * 
                FROM {table_name}
                WHERE urine_timestamp >= TIMESTAMP('{timestamp_start}')
                 AND urine_timestamp <= TIMESTAMP('{timestamp_end}')
            '''.format(table_name=self.table_name, timestamp_start=interval_start, timestamp_end=interval_end).strip()
        table = self.db_instance.fetch_table_by_command(command)
        return table


def test():
    db = DB.from_yaml('../../../db_info.yml')
    table_urine = TableUrineRecords(db)

    table_urine.add_urine_record(status=UrineStatus.abnormal)
    table_urine.add_urine_record(timestamp='2026-01-01 14:00:00', comment='hello Bentley')

    record = table_urine.get_urine_records_by_timestamp('2026-01-01 14:00:00')
    print(record)
    record = table_urine.get_urine_records_by_date('2023-10-22')
    print(record)
    record = table_urine.get_urine_records_by_interval(interval_start='2023-10-19', interval_end='2023-10-24 23:59:59')
    print(record)


if __name__ == '__main__':
    test()
