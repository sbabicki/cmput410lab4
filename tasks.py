from flask import Flask, request, redirect, url_for
import sqlite3
app = Flask(__name__)
dbFile = 'todo.db'
conn = None

def get_conn():
    #tells interpreter to use conn defined above
    global conn
    if conn is None:
        conn = sqlite3.connect(dbFile)
        conn.row_factory = sqlite3.Row
    return conn

@app.teardown_appcontext
def close_connection(exception):
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
    
def add_task(category, priority, description):
    tasks = query_db('insert into tasks values(?,?,?)', [category, priority, description], one = False)
   
    #needed for saving in database
    get_conn().commit()


@app.route('/')
def welcome():
    return '<h1>Welcome to Flask lab (todo3)!</h1>'

@app.route('/task', methods = ['GET', 'POST'])
def task():
   
    #POST
    if request.method == 'POST':
        category = request.form['category']
        priority = request.form['priority']
        description = request.form['description']
        #tasks.append({'category':category})
        add_task(category, priority, description)
        #return redirect('/task1')
        return redirect(url_for('task'))
    
    #GET
    resp = '''
    <form action="" method=post>
    <p>Category: <input type=text name=category></p>
    <p>Priority: <input type=int name=priority></p>
    <p>Description: <input type=text name=description></p>
    <p><input type=submit value=Add></p>
    </form>
    '''
    #Show the table
    resp = resp + '''
    <table border="1" cellpadding="3">
        <tbody>
            <tr>
                <th>Category</th>
                <th>Priority</th>
                <th>Description</th>
            </tr>
    '''
    for task in query_db('select * from tasks'):
        resp = resp + "<tr><td>%s</td><td>%d</td><td>%s</td></tr>" %(task['category'], task['priority'], task['description'])
    resp = resp + '</tbody></table>'
    return resp


if __name__ == '__main__':
    app.debug = True
    app.run()

    