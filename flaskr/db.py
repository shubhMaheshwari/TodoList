import sqlite3

import click
from flask import current_app, g, flash
from flask.cli import with_appcontext
import time
import datetime

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if rv is None:
        return None
    else:
        return (rv[0] if rv else None) if one else rv

def add_new_task(data, user_id):

    db = get_db()
    if db.execute('SELECT id FROM todo_list WHERE title = ?', (data['activity_title'],)).fetchone() is None:
        # the name is available, store it in the database and go to
        # the login page
        query = 'INSERT INTO todo_list(title, body, snooze, Love, Reward, Sleep, Money_Credit, Energy, Stress) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)' 
        db.execute(query,(data['activity_title'],data['description'].strip() , data['snooze'],data['Love_new'], data['Reward_new'], data['Sleep_new'], data['Money_new'], data['Energy_new'], data['Stress_new']))
        db.commit()

    todo = db.execute(
    'SELECT id FROM todo_list WHERE title = ?', (data['activity_title'],)
    ).fetchone()

    # Add deadline default 1 hour
    try:
        print(data['date'], data['time'])
        deadline = datetime.datetime.strptime(data['date'] + ',' +  data['time'] , '%d,%m,%Y,%I:%M%p') - datetime.datetime.now()
        print(deadline, datetime.datetime.strptime(data['date'] + ',' +  data['time'] , '%d,%m,%Y,%H:%M%p'), datetime.datetime.now())
        db.execute('INSERT INTO user_task(user_id, task_id, deadline) VALUES(?, ?,?)',(user_id, todo[0], int(deadline.total_seconds()*60)))        
    except ValueError:
        db.execute('INSERT INTO user_task(user_id, task_id) VALUES(?, ?)',(user_id, todo[0]))
    db.commit()

    

def delete_user_task(data, task_id,user_id):
    db = get_db()

    # Delete task from user_task
    query = 'DELETE FROM user_task WHERE user_id = ? AND task_id = ?'
    db.execute(query,(user_id, task_id))
    db.commit()

    task = query_db('SELECT * FROM todo_list WHERE id = ?', (task_id,), one=True)
    # Update user_emotions
    query = 'UPDATE user SET Love = Love + ?, Reward = Reward + ?, Sleep = Sleep + ?, Money_Credit = Money_Credit + ?, Energy = Energy +  ?, Stress = Stress + ?  WHERE id = ?'
    db.execute(query,(task['Love'], task['Reward'], task['Sleep'],task['Money_Credit'],task['Energy'], task['Stress'], user_id))
    db.commit()