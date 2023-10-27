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

    def fetch_table(self, option: str = 'all'):
        match option:
            case 'all':
                command = 'SELECT * FROM {table_name}'.format(table_name=self.table_name)
            case _:
                command = 'SELECT * FROM {table_name}'.format(table_name=self.table_name)

        table = self.db_instance.fetch_table_by_command(command)
        return table

    def delete_record(self, for_key: str):
        pass

    def update_record(self, for_key: str,  new_dict: dict):
        pass