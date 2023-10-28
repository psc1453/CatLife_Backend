import pymysql.cursors as cursors


def get_column_names_from_cursor(cursor: cursors.Cursor):
    columns = tuple([description[0] for description in cursor.description])
    return columns


def get_table_from_cursor(cursor: cursors.Cursor):
    table_rows_tuple = cursor.fetchall()
    table_rows_list = list(table_rows_tuple)

    column_names = get_column_names_from_cursor(cursor)

    table = [column_names] + table_rows_list

    return table


def parse_sql_value_type(value):
    if isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        if value.strip().upper().startswith(('DATE', 'TIME', 'TIMESTAMP')):
            return value
        else:
            return f'\'{value}\''
    else:
        raise ValueError('Unsupported value type!')


def generate_insert_sql_from_dict(table_name: str, insert_dict: dict):
    from functools import reduce
    sql_key_value_pair = reduce(
        lambda old_pair, new_pair: (', '.join((old_pair[0], new_pair[0])),
                                    ', '.join((old_pair[1], parse_sql_value_type(new_pair[1])))), insert_dict.items(), ('', ''))
    sql_insert_string = 'INSERT INTO {name} ({keys}) VALUES ({values})'.format(name=table_name,
                                                                               keys=sql_key_value_pair[0][2:],
                                                                               values=sql_key_value_pair[1][2:])
    return sql_insert_string
