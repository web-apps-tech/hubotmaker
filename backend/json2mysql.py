#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import MySQLdb as DB
from MySQLdb.cursors import DictCursor as DC

import config


def main():
    conf = load_config()
    schema = load_schema()
    with MySQLdb.connect(**conf['MySQL']) as cursor:
        opts = schema.get('options')
        tables = schema['tables']
        queries = [build_query(name, tbl) for name, tbl in tables.items()]
        print(queries)


def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


def load_schema():
    with open('SQLSchema.json', 'r') as f:
        schema = json.load(f)
    return schema


def build_query(tbl_name, table):
    return 'CREATE TABLE {tbl_name} ({columns});'.format(
        tbl_name=tbl_name,
        columns=', '.join(get_columns(table))
    )


def get_columns(table):
    cols = []
    for colname in table:
        col = table[colname]
        cols.append(
            '{col_name} {data_type}{default_value}{key_idx}{fkey}'.format(
                col_name=colname,
                data_type=get_datatype(col),
                default_value=get_default(col),
                key_idx=get_key_index(col),
                fkey=get_foreign_key(colname, col)
            )
        )
    return cols


def get_datatype(col):
    INTEGER = ['TINYINT', 'SMALLINT', 'MEDIUMINT', 'INT', 'INTEGER', 'BIGINT']
    FLOAT = ['FLOAT', 'DOUBLE', 'DOUBLE PRECISION', 'REAL']
    DATETIME = ['DATE', 'DATETIME', 'TIMESTAMP', 'TIME', 'YEAR']
    CHARACTER = ['CHARACTER', 'CHAR', 'CHARACTER VARYING', 'VARCHAR']
    BINARY = ['BINARY', 'CHAR BYTE', 'VARBINARY']
    BLOB = ['TINYBLOB', 'BLOB', 'MEDIUMBLOB', 'LONGBLOB']
    TEXT = ['TINYTEXT', 'TEXT', 'MEDIUMTEXT', 'LONGTEXT']

    low_dtype = col['type']
    dtype = col['type'].upper()
    if (dtype in INTEGER + FLOAT):
        dtype += ' UNSIGNED' if col.get('unsigned') else ''
        dtype += ' ZEROFILL' if col.get('zerofill') else ''
    elif dtype in CHARACTER:
        dtype += '(' + str(col.get('max_length', 128)) + ')'
        dtype += get_charset(col)
    elif dtype in BINARY + DATETIME:
        pass
    elif dtype in BLOB + TEXT:
        dtype += get_charset(col)
    elif dtype in ['ENUM', 'SET']:
        listname = low_dtype + 'list'
        dtype += '(' + ', '.join(["'" + e + "'" for e in col[listname]]) + ')'
        if col.get('charset'):
            dtype += ' CHARACTER SET ' + col['charset']
    return dtype


def get_charset(col):
    if col.get('ascii'):
        return ' ASCII'
    elif col.get('unicode'):
        return ' UNICODE'
    elif col.get('binary'):
        return ' BINARY'
    elif col.get('charset'):
        return ' CHARACTER SET {}'.format(col['charset'])
    else:
        return ''


def get_default(col):
    if col.get('default'):
        return ' DEFAULT ' + col['default']
    return ''


def get_key_index(col):
    key = ''
    if col.get('primary key'):
        key += ' PRIMARY KEY'
    if col.get('not null'):
        key += ' NOT NULL'
    if col.get('unique'):
        key += ' UNIQUE'
    return key


def get_foreign_key(colname, col):
    if col.get('foreign key'):
        fk = col['foreign key']
        return ' FOREIGN KEY ({}) REFERENCES {} [{}]{}{}'.format(
            colname,
            fk['table'],
            fk['col'],
            ' ON DELETE ' + fk['on delete'] if fk.get('on delete') else ''
            ' ON UPDATE ' + fk['on update'] if fk.get('on update') else ''
        )
    else:
        return ''


if __name__ == '__main__':
    main()
