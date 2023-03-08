from flask import Flask, request, jsonify
from flask_cors import CORS 
import json, mysql.connector
app = Flask(__name__)
CORS(app)

def access_to_bdd(command,return_element):
     with open('config.json') as json_file:
         data = json.load(json_file)
     conn = mysql.connector.connect(**data)
     cursor = conn.cursor()
     cursor.execute(command)
     if return_element ==True:
       employees = []
       rows = cursor.fetchall()
       for row in rows:
          employee = {"id": row[0], "firstName": row[1], "lastName": row[2], "emailId": row[3]}
          employees.append(employee)
       conn.commit()  
       conn.close()
       return employees
     else:
       conn.commit()
       conn.close()

access_to_bdd(" CREATE TABLE IF NOT EXISTS employees (employee_id INT PRIMARY KEY AUTO_INCREMENT, firstname VARCHAR(50)  NULL, lastname VARCHAR(50) NULL, emailid VARCHAR(100) );",False)
employeees =  access_to_bdd("select * from employees",True)#pour les testes unitaires
@app.route('/', methods=['GET'])
def index():
    return "bienvenue sur mon super api"
@app.route('/api/v1/employees', methods=['GET','POST'])  
def manage_products(): 
    if request.method == 'GET':
        prods =access_to_bdd("select * from employees",True)
        return jsonify(prods)
    else :
     employee = request.get_json()
     fn = employee['firstName']
     ln = employee['lastName']
     emid = employee['emailId']

     if request.method == 'POST':
        command = "Insert into employees(firstname,lastname,emailid) values( '"+fn+"' , '"+ln+"' , '"+emid +"' )"
        print(command)
        access_to_bdd(command,False)
        return jsonify({'result': 'Product added'})
    
     
     
@app.route('/api/v1/employees/<int:id>', methods=['GET','PUT','DELETE'])  
def manage_product(id):
     if request.method == 'GET':
        command ="select *  from employees where employee_id = "+ str(id)
        prods =access_to_bdd(command,False)
        print(prods)
        return jsonify(prods)
     if request.method == 'DELETE':
        command ="Delete  from employees where employee_id = "+ str(id)
        print(command)
        access_to_bdd(command,False)
        return jsonify({'result': 'Product deleted'})
     
     if request.method == 'PUT':
        employee = request.get_json()
        fn = employee['firstName']
        ln = employee['lastName']
        emid = employee['emailId']
        command ="update employees set firstname = '"+ fn+"' , lastname = '"+ln+"' , emailid = '"+emid +"' "+ " where employee_id = "+ str(id)
        access_to_bdd(command,False)
        return jsonify({'result': 'Product updated'})
    
     else :
        return jsonify ({'result': 'bad request'})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8081 ,debug=True)