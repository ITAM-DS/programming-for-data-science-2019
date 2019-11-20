#! /usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras

import sys
from datetime import timedelta

import click

from dynaconf import settings

from pathlib import Path

@click.group()
@click.pass_context
def berka(ctx):
    ctx.ensure_object(dict)
    conn = psycopg2.connect(settings.get('DBURL'))
    #ctx.obj['conn'] = conn

    queries = {}
    for sql_file in Path('sql').glob('*.sql'):
        with open(sql_file,'r') as sql:
            sql_key = sql_file.stem
            query = str(sql.read())
            queries[sql_key] = query
    print(queries.keys())
    ctx.obj['queries'] = queries

@berka.command()
@click.pass_context
def create_schemas(ctx):
    query = ctx.obj['queries'].get('create_schemas')
    print(query)


@berka.command()
@click.pass_context
def create_raw_tables(ctx):
    query = ctx.obj['queries'].get('create_raw_tables')
    print(query)

@berka.command()
@click.pass_context
def load_berka(ctx):
    conn = ctx.obj['conn']
    with conn.cursor() as cursor:
        # lee cada uno de los archivos
        cursors.copy_from(obj, table, sep=';')

if __name__ == '__main__':
    berka()
