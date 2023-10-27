import pymysql
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
