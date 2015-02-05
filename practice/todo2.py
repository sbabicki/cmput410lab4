#from flask import Flask, request, redirect, url_for

import sqlite3
dbFile = 'tasks.db'
conn = None

def get_conn():
    #tells interpreter to use conn defined above
    global conn
    if conn is None:
        conn = sqlite3.connect(dbFile)
        conn.row_factory = sqlite3.Row
    return conn

def close_connection():
    global conn
    if conn is not None:
        conn.close()
        conn = None
        
def query_db(query, args=(), one=False):
    cur = get_conn().cursor()
    cur.execute(query, args)
    #result
    r = cur.fetchall()
    cur.close()
    return (r[0] if r else None) if one else r
    
def add_task(category):
    tasks = query_db('insert into tasks(category) values(?)', [category], one = True)
   
    #needed for saving in database
    get_conn().commit()
    
def print_tasks():
    tasks = query_db('select * from tasks')
    for task in tasks:
        print("Task(category): %s"%task['category'])
    print("%d tasks in total."%len(tasks))


if __name__ == '__main__':
    query_db('delete from tasks')
    print_tasks()
    add_task('test')
    add_task('test2')
    add_task('test3')
    add_task('test4')
    print_tasks()
    
    