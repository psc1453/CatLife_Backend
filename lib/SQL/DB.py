import pymysql

from .utils import get_table_from_cursor, generate_insert_sql_from_dict, generate_delete_sql_from_key


class DB:
    def __init__(self, host, port, name, user, password):
        self.db_host = host
        self.db_port = port
        self.db_name = name
        self.db_user = user
        self.db_password = password

    @classmethod
    def from_yaml(cls, yaml_file):
        from ruamel.yaml import YAML

        with open(yaml_file, 'r') as db_info_yaml:
            yaml = YAML(typ='safe')
            db_info = yaml.load(db_info_yaml)

        assert all((key in ['host', 'port', 'name', 'user', 'password']) for key in list(
            db_info.keys())), 'YAML file does not contains some of values in [host, port, name, user, password].'

        return cls(host=db_info['host'], port=db_info['port'], name=db_info['name'], user=db_info['user'],
                   password=db_info['password'])

    def fetch_table_by_command(self, command: str):
        assert command.strip().upper().startswith(
            'SELECT'), 'Not a command for fetching data which begins with SELECT statement.'
        db_connection = pymysql.connect(host=self.db_host, port=self.db_port, database=self.db_name, user=self.db_user,
                                        password=self.db_password)
        db_cursor = db_connection.cursor()
        db_cursor.execute(command)
        table = get_table_from_cursor(db_cursor)

        db_cursor.close()
        db_connection.close()
        return table

    def insert_row_to_table_by_command(self, command: str):
        assert command.strip().upper().startswith(
            'INSERT'), 'Not a command for inserting data which begins with INSERT statement.'
        db_connection = pymysql.connect(host=self.db_host, port=self.db_port, database=self.db_name, user=self.db_user,
                                        password=self.db_password)
        db_cursor = db_connection.cursor()
        try:
            db_cursor.execute(command)
            db_connection.commit()
        except Exception as error:
            print('Failed inserting data:', error)
            db_connection.rollback()
            raise error

        db_cursor.close()
        db_connection.close()

    def insert_row_to_table_by_dict(self, table_name, insert_dict):
        command = generate_insert_sql_from_dict(table_name, insert_dict)
        self.insert_row_to_table_by_command(command)

    def delete_row_from_table_by_command(self, command: str):
        assert command.strip().upper().startswith(
            'DELETE'), 'Not a command for deleting data which begins with DELETE statement.'
        db_connection = pymysql.connect(host=self.db_host, port=self.db_port, database=self.db_name, user=self.db_user,
                                        password=self.db_password)
        db_cursor = db_connection.cursor()
        try:
            db_cursor.execute(command)
            db_connection.commit()
        except Exception as error:
            print('Failed deleting row: ', error)
            db_connection.rollback()
            raise error

        db_cursor.close()
        db_connection.close()

    def delete_row_from_table_by_key(self, table_name, key_name, key_value):
        command = generate_delete_sql_from_key(table_name, key_name, key_value)
        self.delete_row_from_table_by_command(command)
