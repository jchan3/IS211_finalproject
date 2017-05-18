"""Docstring for Joe Chan: schema.sql"""

drop table if exists entries;
CREATE TABLE entries (id INTEGER PRIMARY KEY ASC,
                title TEXT not null,
                blogpost TEXT not null,
                author TEXT,
                date DATE);


