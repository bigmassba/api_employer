import mysql.connector ,json
from flask import Flask, request, jsonify
class connectdb:
   
   def log_on_db(command):
        with open('config.json') as json_file:
             data = json.load(json_file)
        conn = mysql.connector.connect(**data)
        cursor = conn.cursor()
        cursor.execute(command)
        cursor.execute("select * from employees")
        employees = []
        rows = cursor.fetchall()
        for row in rows:
            employee = {"id": row[0], "firstName": row[1], "lastName": row[2], "emailId": row[3]}
            employees.append(employee)
            return(employees)

        conn.commit()  
        conn.close() 

       
            
  

 



