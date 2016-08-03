#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import pymysql as DB

import config


def main():
    schema = load_schema()
    with DB.connect(**config.MySQL) as cursor:
        opts = schema.get('options')
        tables = schema['tables']
        queries = [build_query(name, tbl) for name, tbl in tables.items()]
        for query in queries:
            cursor.execute(query)


def load_schema():
    with open('../spec/SQLSchema.json', 'r') as f:
        schema = json.load(f)
    return schema


def build_query(tbl_name, table):
    return 'CREATE TABLE {tbl_name} ({columns}{foreign_key});'.format(
        tbl_name=tbl_name,
        columns=', '.join(get_columns(table)),
        foreign_key=get_foreign_key(table.get('foreign_key'))
    )


def get_columns(table):
    cols = []
    for col in table['columns']:
        cols.append(
            '{col_name} {data_type}{default_value}{key_idx}'.format(
                col_name=col['name'],
                data_type=get_datatype(col),
                default_value=get_default(col),
                key_idx=get_key_index(col),
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


def get_foreign_key(fk):
    if fk is not None:
        return ', FOREIGN KEY ({}) REFERENCES {}({}){}{}'.format(
            fk['key'],
            fk['ref_table'],
            fk['ref_col'],
            ' ON DELETE ' + fk.get('on delete') if fk.get('on delete') else '',
            ' ON UPDATE ' + fk.get('on update') if fk.get('on update') else ''
        )
    else:
        return ''

if __name__ == '__main__':
    main()
