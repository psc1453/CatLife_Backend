from lib.SQL.DB import DB
from lib.SQL.ViewOperations.DBViewProtocol import DBViewProtocol


class ViewDietEveryday(DBViewProtocol):
    def __init__(self, db_instance: DB):
        super().__init__(db_instance)

    @property
    def VIEW_NAME(self):
        return 'DietEverydayView'

    @property
    def READABLE_COLUMNS(self):
        return ['diet_date', 'food_category', 'total_quantity']

    def fetch_record(self, for_key: str):
        command = f'''
            SELECT *
            FROM {self.VIEW_NAME}
            WHERE diet_date = {for_key}
        '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def get_diet_records_by_date(self, date: str):
        command = f'''
            SELECT * 
            FROM {self.VIEW_NAME}
            WHERE diet_date = DATE('{date}')
        '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    def get_diet_records_by_interval(self, interval_start: str = None, interval_end: str = None):
        if (interval_start, interval_end) == (None, None):
            command = f'''
                SELECT * FROM {self.VIEW_NAME}
            '''
        elif interval_start is not None and interval_end is None:
            command = f'''
                SELECT * 
                FROM {self.VIEW_NAME}
                WHERE diet_date >= TIMESTAMP('{interval_start}')
            '''
        elif interval_start is None and interval_end is not None:
            command = f'''
                SELECT * 
                FROM {self.VIEW_NAME}
                WHERE diet_date <= TIMESTAMP('{interval_end}')
            '''
        else:
            command = f'''
                SELECT * 
                FROM {self.VIEW_NAME}
                WHERE diet_date >= TIMESTAMP('{interval_start}')
                 AND diet_date <= TIMESTAMP('{interval_end}')
            '''
        table = self.db_instance.fetch_table_by_command(command)
        return table


def test():
    db = DB.from_yaml('../../../db_info.yml')
    view_diet = ViewDietEveryday(db)

    record = view_diet.get_diet_records_by_date('2023-10-22')
    print(record)
    record = view_diet.get_diet_records_by_interval(interval_start='2023-10-19', interval_end='2023-10-24 23:59:59')
    print(record)


if __name__ == '__main__':
    test()
