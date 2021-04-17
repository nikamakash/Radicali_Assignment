# import Required library, modules
from flask import Flask, jsonify, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'akash'


# Index Page of Of System
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to Inventory Management Radicali Assignment"})


# Login for Employee
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        conn = sqlite3.connect('invent.db')
        cursor = conn.cursor()
        cursor.execute('select id, name, password from Employee;')
        data = cursor.fetchall()
        session['id'] = None
        for i in data:
            if i[1] == username and i[2] == password:
                session['id'] = i[0]
                break
        if session['id'] is not None:
            return jsonify({'Success': 'Logged in Successfully...'})
        return jsonify({'Error': 'Invalid Credentials...'})

    return jsonify({'Message': 'No Data Found'})


"""Dashboard for Manager"""


@app.route("/manager", methods=['GET'])
def dashboard():
    """ this will show Equipment name and status (ie. Issued or Not) """
    conn = sqlite3.connect('invent.db')
    cursor = conn.cursor()
    cursor.execute('select name, status from Invents;')
    result = cursor.fetchall()
    conn.close()
    return jsonify({'data': result})


@app.route("/manager/requests", methods=['GET'])
def requests():
    """ this function shows all requests by Employee for Equipments"""
    conn = sqlite3.connect('invent.db')
    cursor = conn.cursor()
    cursor.execute('select name,requests from Employee;')
    result = cursor.fetchall()
    conn.close()
    return jsonify({'data': result})


""" Employee Dashborard """

@app.route("/employee", methods=['GET', 'POST'])
def issue_invent():
    """ this will Issue an Equipment """
    if request.method == ['POST']:
        invent_id = request.form['id']
        conn = sqlite3.connect('invent.db')
        cursor = conn.cursor()
        cursor.execute('insert into Invents(employee) values(?);', (session['id'],))
        conn.commit()
        conn.close()
        return jsonify({'Success': 'Invent Issued successfully'})

    # this will show available Equipments

    conn = sqlite3.connect('invent.db')
    cursor = conn.cursor()
    cursor.execute('select name from Invents where qty>0;')
    result = cursor.fetchall()
    conn.close()
    return jsonify({'data': result})


@app.route("/employee/return", methods=['GET', 'POST'])
def return_invent():
    """ function for Returning an Isued Eqipment to manager"""
    if request.method == ['POST']:
        invent_id = request.form['id']
        conn = sqlite3.connect('invent.db')
        cursor = conn.cursor()
        cursor.execute('insert into Invents(employee) values(?);', (session['id'],))
        conn.commit()
        conn.close()
        return jsonify({'Success': 'Invent Returned successfully'})
    conn = sqlite3.connect('invent.db')
    cursor = conn.cursor()
    cursor.execute('select name from Invents where employee=?;', (session['id'],))
    result = cursor.fetchall()
    return jsonify({'data': result})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
