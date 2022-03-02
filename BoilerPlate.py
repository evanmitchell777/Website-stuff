from flask import Flask,render_template,request,session,redirect,url_for
import socket
from datetime import datetime
import os
from time import sleep
import hashlib as algo
import sqlite3 as sql


BoilerPlate = Flask(__name__)
BoilerPlate.secret_key = os.urandom(32)


@BoilerPlate.route('/', methods=["GET","POST"])
def index():
    return render_template('index.html')


@BoilerPlate.route('/loginprim', methods=['GET','POST'])
def login():
    #----Form-Data-------------------
    username=request.form['Username']
    password=request.form['Password']
    cipherofuser = algo.sha256(username.encode())
    cipherofpass = algo.sha256(password.encode())
    #--------------------------------
    #----DB-Data---------------------
    seqfmtu = (str(username,))
    seqfmtp = (str(cipherofpass,))
    #--------Grab-password-----------
    try:
        init = sql.connect('users.db')
        cursor = init.cursor()
        cursor.execute("SELECT * FROM UserData WHERE username=?",(seqfmtu,))
        datapull = cursor.fetchall()
        combed_data = datapull[0]
        db_pass = combed_data[1]
    except:
        return render_template('authfail.html')
    #--------------------------------
    if cipherofpass.hexdigest() == db_pass: 
        session['byuser'] = str(username)
        cursor.close()
        if 'byuser' in session:
            with open('sessionlog.txt','w') as sessionlog:
                sessionlog.write(str(session['byuser'])+'\n')
            sessionlog.close()
            session['authtoken'] = True
            return render_template('welcome.html')
        else:
            return redirect('insession:false')
    else:
        return redirect('/insession:false')


@BoilerPlate.route('/welcome')
def welcome():
    if 'byuser' in session and 'authtoken' in session:
        return render_template('welcome.html')
    else:
        return redirect('/ insession:false')

@BoilerPlate.route('/insession:false', methods=['GET','POST'])
def auth_fail():
    if request.method=='POST':
        if request.form['button'] == 'Return to Home':
            return render_template('index.html')
    elif request.method == 'GET':
        return render_template('authfail.html')

if __name__ == "__main__":
    BoilerPlate.run(host="localhost", port=8080, debug=True) 
