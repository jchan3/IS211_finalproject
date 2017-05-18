#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Docstring for Joe Chan: chanproject.py"""


import time
import datetime
import os
import sqlite3
import re
from flask import Flask, render_template
from flask import request, session, g, redirect, url_for, abort, flash
from contextlib import closing


DATABASE = 'chanproject.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)

app.config.from_object(__name__)
app.config.from_envvar('Flaskr_settings', silent=True)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('select title, blogpost, author, date from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        if user != app.config['USERNAME']:
            error = 'Invalid username'
        elif password != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            username = user
            session['username'] = user
            return redirect('/dashboard')
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect('/login')


@app.route('/dashboard/')
def dashboard():
    cur = g.db.execute('select id, title, blogpost, author, date from entries order by id desc')
    entries = cur.fetchall()
    return render_template('dashboard.html', entries=entries)


@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    user = session['username']
    userlist = []
    userlist.append(str(user))
    dateformat = "%Y-%m-%d"
    today = datetime.date.today()
    s = today.strftime(dateformat)
    d = datetime.datetime.strptime(s, dateformat)

    if not session.get('logged_in'):
        abort(401)
    try:
        if request.method == 'POST':
            title = request.form['title']
            blogpost = request.form['blogpost']
            author = request.form['author']
            g.db.execute('insert into entries (title, blogpost, author, date) values (?,?,?,?)',
                         [title, blogpost, author, d])
            g.db.commit()
            return redirect('/dashboard')
    except:
        flash('Error Encountered')
    return render_template('addpost.html', userlist=userlist)


@app.route('/edit/<postid>', methods=['GET', 'POST'])
def edit_post(postid):
    sql = "SELECT id, title, blogpost FROM entries \
            WHERE id=:id"

    cur = g.db.execute(sql, {"id": postid})
    results = cur.fetchall()
    return render_template('edit_post.html', results=results)


@app.route('/update', methods=['GET', 'POST'])
def update_entry():
    sql = "UPDATE entries SET title = (?), blogpost = (?) WHERE id = (?)"

    if not session.get('logged_in'):
        abort(401)
    try:
        if request.method == 'POST':
            pid = request.form['pid']
            newtitle = request.form['title']
            newblog = request.form['blogpost']
            g.db.execute(sql, (newtitle, newblog, pid))
            g.db.commit()
            return redirect('/dashboard')
    except:
        flash('Error Encountered')
    return render_template('edit_post.html')


@app.route('/delete/<postid>', methods=['GET', 'POST'])
def delete_post(postid):
    sql = "DELETE FROM entries WHERE id=:id"

    if not session.get('logged_in'):
        abort(401)
    try:
        g.db.execute(sql, {"id": postid})
        g.db.commit()
        return redirect('/dashboard')
    except:
        flash('Error Encountered')
    return render_template('edit_post.html')


if __name__ == '__main__':
    app.run()
