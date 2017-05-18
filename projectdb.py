#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Docstring for Joe Chan: projectdb.py"""


import sqlite3 as lite
import sys


con = lite.connect('chanproject.db')


with con:

    cur = con.cursor()

    sql = """CREATE TABLE entries (id INTEGER PRIMARY KEY ASC,
                title TEXT not null, blogpost TEXT not null,
                author TEXT, date DATE);"""

    cur.execute(sql)
