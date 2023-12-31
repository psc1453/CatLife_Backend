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
    def TABLE_NAME(self):
        return 'UrineRecords'

    @property
    def EDITABLE_COLUMNS(self):
        return ['urine_timestamp', 'urine_status', 'urine_comment']

    @property
    def PRIMARY_KEY(self):
        return 'urine_id'

    @property
    def FOREIGN_KEYS(self):
        return []

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

    def get_urine_records_all(self):
        return self.fetch_table()

    def get_urine_record_by_id(self, urine_id: int):
        return self.fetch_record(urine_id)

    def get_urine_record_by_timestamp(self, timestamp: str):
        command = f'''
                    SELECT *
                    FROM {self.TABLE_NAME}
                    WHERE urine_timestamp = TIMESTAMP(\'{timestamp}\')
        '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def get_urine_records_by_date(self, date: str):
        command = f'''
            SELECT * 
            FROM {self.TABLE_NAME}
            WHERE DATE(urine_timestamp) = DATE('{date}')
        '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def get_urine_records_by_interval(self, interval_start: str = None, interval_end: str = None):
        if (interval_start, interval_end) == (None, None):
            command = f'''
                SELECT * FROM {self.TABLE_NAME}
            '''
        elif interval_start is not None and interval_end is None:
            command = f'''
                SELECT * 
                FROM {self.TABLE_NAME}
                WHERE urine_timestamp >= TIMESTAMP('{interval_start}')
            '''
        elif interval_start is None and interval_end is not None:
            command = f'''
                SELECT * 
                FROM {self.TABLE_NAME}
                WHERE urine_timestamp <= TIMESTAMP('{interval_end}')
            '''
        else:
            command = f'''
                SELECT * 
                FROM {self.TABLE_NAME}
                WHERE urine_timestamp >= TIMESTAMP('{interval_start}')
                 AND urine_timestamp <= TIMESTAMP('{interval_end}')
            '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def delete_urine_record_by_id(self, urine_id: int):
        self.delete_record(urine_id)

    def update_urine_record_by_id_with_dict(self, urine_id: int, update_dict: dict):
        self.update_record(urine_id, update_dict)


def test():
    db = DB.from_yaml('../../../db_info.yml')
    table_urine = TableUrineRecords(db)

    table_urine.add_urine_record(status=UrineStatus.abnormal)
    table_urine.add_urine_record(timestamp='2026-01-01 14:00:00', comment='hello Bentley')

    record = table_urine.get_urine_record_by_timestamp('2026-01-01 14:00:00')
    print(record)
    record = table_urine.get_urine_records_by_date('2023-10-22')
    print(record)
    record = table_urine.get_urine_records_by_interval(interval_start='2023-10-19', interval_end='2023-10-24 23:59:59')
    print(record)


if __name__ == '__main__':
    test()
