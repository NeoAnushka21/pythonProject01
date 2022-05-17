from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('mysqlsampledatabase.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def student_form():
    try:
        conn = get_db_connection()
        details = conn.execute("SELECT * FROM stud_data ORDER BY id")
        conn.close()
        return render_template('index.html', details=details)
    except Exception as e:
        print(e)
        return "<h3 style='color:red'><b>opps something went wrong while directing to home page</b></h3>"


@app.route("/add_student", methods=["POST", "GET"])
def add_student():
    try:
        cursor = mysql_connector.connection.cursor()
        cur = mysql_connector.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            student_name = request.form['student_name']
            student_department = request.form['student_department']
            student_email = request.form['student_email']
            print(student_name)
            if student_name == '':
                msg = '<h4 style="color:red"><b>Error !! Name missing</b></h4>'
            elif student_department == '':
                msg = '<h3 style="color:red"><b>Error !! Department missing</b></h3>'
            elif student_email == '':
                msg = '<h3 style="color:red"><b>Error !! Email missing</b></h3>'
            else:
                cur.execute("INSERT INTO stud_data (name,department,email) VALUES (%s,%s,%s)",
                            [student_name, student_department, student_email])
                mysql_connector.connection.commit()
                cur.close()
                msg = '<h3 style="color:green"></b>Student details added successfully</b></h3>'
        return jsonify(msg)
    except Exception as e:
        return '<h2 style="color:red"><b>Email already exists change it</b></h2>'


@app.route("/update_student", methods=["POST", "GET"])
def update_student():
    try:

        cursor = mysql_connector.connection.cursor()
        cur = mysql_connector.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            string = request.form['string']
            student_name = request.form['student_name']
            student_department = request.form['student_department']
            student_email = request.form['student_email']
            print(string)
            cur.execute("UPDATE stud_data SET name = %s, department = %s,email = %s WHERE id = %s ",
                        [student_name, student_department, student_email, string])
            mysql_connector.connection.commit()
            cur.close()
            msg = '<h3 style="color:green"><b>Record successfully Updated</b></h3>'
        return jsonify(msg)
    except Exception as e:
        print(e)
        return '<h2 style="color:red"><b>Email already exists change it</b></h2>'


@app.route("/delete_student", methods=["POST", "GET"])
def delete_student():
    try:
        cursor = mysql_connector.connection.cursor()
        cur = mysql_connector.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            getid = request.form['string']
            print(getid)
            cur.execute('DELETE FROM stud_data WHERE id = {0}'.format(getid))
            mysql_connector.connection.commit()
            cur.close()
            msg = '<h3 style="color:green"><b>Record successfully deleted</b></h3>'
        return jsonify(msg)
    except Exception:
        return '<h3 style="color:red"><b>Something went wrong while deleting student details</b></h3>'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
