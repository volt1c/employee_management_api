import json
import datetime
from db import mysql


class Employee:
    @staticmethod
    def get_all():
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        cursor.close()
        return rows

    @staticmethod
    def get_by_id(employee_id):
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id=%s", (employee_id,))
        row = cursor.fetchone()
        cursor.close()
        return row

    @staticmethod
    def add(name, email):
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cursor.close()


class Schedule:
    @staticmethod
    def get_by_employee_id(employee_id):
        conn = mysql.connect
        cursor = conn.cursor()
        date_format = "%d-%m-%Y"
        cursor.execute("""SELECT id, employee_id, 
        DATE_FORMAT(entry_time, %s) AS entry_time, 
        DATE_FORMAT(exit_time, %s) AS exit_time 
        FROM schedules WHERE employee_id=%s""", (date_format, date_format, employee_id))
        row_headers = [x[0] for x in cursor.description] # this will extract row headers
        rv = cursor.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json_data

    @staticmethod
    def add_entry(employee_id, entry_time):
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("INSERT INTO schedules (employee_id, entry_time) VALUES (%s, %s)", (employee_id, entry_time))
        conn.commit()
        cursor.close()

    @staticmethod
    def add_exit(schedule_id, exit_time):
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("UPDATE schedules SET exit_time=%s WHERE id=%s", (exit_time, schedule_id))
        conn.commit()
        cursor.close()
