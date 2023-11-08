from enum import Enum
from typing import Union

from lib.SQL.DB import DB
from lib.SQL.TableOperations.DBTableProtocol import DBTableProtocol


class StoolStatus(Enum):
    normal = 0
    hard = 1
    soft = 2
    liquid = 3


class TableStoolRecords(DBTableProtocol):
    def __init__(self, db_instance: DB):
        super().__init__(db_instance)

    @property
    def TABLE_NAME(self):
        return 'StoolRecords'

    @property
    def EDITABLE_COLUMNS(self):
        return ['stool_timestamp', 'stool_status', 'stool_comment']

    @property
    def PRIMARY_KEY(self):
        return 'stool_id'

    @property
    def FOREIGN_KEYS(self):
        return []

    def insert_record(self, insert_dict: dict):
        assert all((key in self.EDITABLE_COLUMNS) for key in list(
            insert_dict.keys())), \
            'Find unsupported keys, only [stool_timestamp, stool_status, stool_comment] are supported'

        self.db_instance.insert_row_to_table_by_dict(self.TABLE_NAME, insert_dict)

    def fetch_record(self, for_key: int):
        command = f'''
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE stool_id = {for_key}
        '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    # TODO: Add the delete and update functions.

    def update_record(self, for_key: int, new_dict: dict):
        pass

    def add_stool_record(self, timestamp: str = None, status: Union[StoolStatus, str] = StoolStatus.normal,
                         comment: str = None):
        """

        :param timestamp: Only support format like '2023-10-27 10:34:07'
        :param status: Enum(StoolStatus.normal, StoolStatus.hard, StoolStatus.soft, StoolStatus.liquid)
        :param comment:
        :return:
        """
        status_str = status if type(status) == str else status.name
        assert status_str in [s.name for s in StoolStatus], \
            ('Not a valid option for parameter \'status\'! '
             'Only [hard, normal, soft, liquid] are support, or using StoolStatus which is more recommended!')
        insert_dict = {'stool_status': status_str}
        if timestamp is not None:
            insert_dict.update({'stool_timestamp': timestamp})
        if comment is not None:
            insert_dict.update({'stool_comment': comment})
        self.insert_record(insert_dict)

    def get_stool_records_all(self):
        command = f'''
            SELECT * 
            FROM {self.TABLE_NAME}
        '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def get_stool_record_by_id(self, stool_id: int):
        return self.fetch_record(stool_id)

    def get_stool_record_by_timestamp(self, timestamp: str):
        command = f'''
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE stool_timestamp = TIMESTAMP(\'{timestamp}\')
        '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def get_stool_records_by_date(self, date: str):
        command = f'''
            SELECT * 
            FROM {self.TABLE_NAME}
            WHERE DATE(stool_timestamp) = DATE('{date}')
        '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def get_stool_records_by_interval(self, interval_start: str = None, interval_end: str = None):
        if (interval_start, interval_end) == (None, None):
            command = f'''
                SELECT * FROM {self.TABLE_NAME}
            '''
        elif interval_start is not None and interval_end is None:
            command = f'''
                SELECT * 
                FROM {self.TABLE_NAME}
                WHERE stool_timestamp >= TIMESTAMP('{interval_start}')
            '''
        elif interval_start is None and interval_end is not None:
            command = f'''
                SELECT * 
                FROM {self.TABLE_NAME}
                WHERE stool_timestamp <= TIMESTAMP('{interval_end}')
            '''
        else:
            command = f'''
                SELECT * 
                FROM {self.TABLE_NAME}
                WHERE stool_timestamp >= TIMESTAMP('{interval_start}')
                 AND stool_timestamp <= TIMESTAMP('{interval_end}')
            '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def delete_stool_record_by_id(self, stool_id: int):
        self.delete_record(stool_id)


def test():
    db = DB.from_yaml('../../../db_info.yml')
    table_stool = TableStoolRecords(db)

    table_stool.add_stool_record(status=StoolStatus.hard)
    table_stool.add_stool_record(timestamp='2026-01-01 14:00:00', comment='hello Bentley')

    record = table_stool.get_stool_record_by_timestamp('2026-01-01 14:00:00')
    print(record)
    record = table_stool.get_stool_records_by_date('2023-10-22')
    print(record)
    record = table_stool.get_stool_records_by_interval(interval_start='2023-10-19', interval_end='2023-10-24 23:59:59')
    print(record)


if __name__ == '__main__':
    test()
