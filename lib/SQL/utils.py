from typing import Union

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
    if value is None or value == '':
        return 'NULL'
    else:
        if isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            if value.strip().upper().startswith(('DATE', 'TIME', 'TIMESTAMP')):
                return value
            else:
                return f'\'{value}\''
        else:
            print(type(value))
            raise ValueError(f'Unsupported value type! {type(value)} is not supported while parsing to SQL syntax!')


def generate_sql_key_value_pair_for_insert(dict_input: dict):
    from functools import reduce
    sql_key_value_pair = reduce(
        lambda old_pair, new_pair: (', '.join((old_pair[0], new_pair[0])),
                                    ', '.join((old_pair[1], parse_sql_value_type(new_pair[1])))),
        dict_input.items(),
        ('', ''))
    return sql_key_value_pair[0][2:], sql_key_value_pair[1][2:]


def generate_sql_key_value_string_for_update(dict_input: dict):
    from functools import reduce
    sql_key_value_string = reduce(
        lambda old_str, new_pair: ', '.join(
            (old_str,
             ' = '.join(
                 (new_pair[0], parse_sql_value_type(new_pair[1]))
             ))
        ),
        dict_input.items(),
        ''
    )
    return sql_key_value_string[2:]


def generate_insert_sql_from_dict(table_name: str, insert_dict: dict):
    sql_key_value_pair = generate_sql_key_value_pair_for_insert(insert_dict)
    sql_insert_string = f'''
        INSERT INTO {table_name}
        ({sql_key_value_pair[0]})
        VALUES 
        ({sql_key_value_pair[1]})
    '''
    print(sql_key_value_pair)
    return sql_insert_string


def generate_delete_sql_from_key(table_name: str, key_name: str, key_value: Union[str, int]):
    sql_delete_string = f'''
        DELETE FROM {table_name}
        WHERE {key_name} = {parse_sql_value_type(key_value)}
    '''
    return sql_delete_string


def generate_update_sql_by_key_with_dict(table_name: str, key_name: str, key_value: Union[str, int], update_dict: dict):
    sql_key_value_string = generate_sql_key_value_string_for_update(update_dict)
    sql_update_string = f'''
        UPDATE {table_name}
        SET {sql_key_value_string}
        WHERE {key_name} = {parse_sql_value_type(key_value)}
    '''
    return sql_update_string
