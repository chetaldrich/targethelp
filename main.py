import os
import random
import twilio.twiml

from sqlite3     import dbapi2
from flask       import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup
from contextlib  import closing
from twilio.rest import TwilioRestClient
from pprint      import pprint
from send_sms    import sms

# Constants
DATABASE = 'messages.db'
DEBUG = True
SECRET_KEY = 'pass'

# App configuration
app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)

# Script for initialising database with ./schema.sql
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def connect_db():
    return dbapi2.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/monitor')
def show_wimpers():
    cur = get_db().execute('select * from wimpers order by id desc')
    stuff  = cur.fetchall()
    cur.close()
    return render_template('index.html', W = stuff)

@app.route("/", methods=['GET', 'POST'])
def add_wimper():
    resp = twilio.twiml.Response()
    msg = str(request.values['Body'])
    l = msg.split("#")
    aile = l[0]
    xname = l[1]
    xmessage = l[2]

    e_number = random.randint(0,13)
    employee = ["billy","Sam","Anna","Chet","Taylor","Saba","Sam","Nick","Joe","Samantha","Robert","Bob","Ken","David"]
    xemployee = employee[e_number]
    xstatus = "waiting"
    mid = ". An agent will be with you in a moment! You said "
    sms()
    resp.message("Hello " + xname + mid + xmessage)
    g.db.execute('insert into wimpers (num, name, message, employee, status) values (?,?,?,?,?)', [aile, xname, xmessage, xemployee, xstatus])
    g.db.commit()
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
