from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Aiven MySQL configurations
app.config['MYSQL_HOST'] = 'iqindia-sanskariqindia-01c1.i.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_d9OgBQ5g5eQBAIW07TH'
app.config['MYSQL_DB'] = 'defaultdb'
app.config['MYSQL_PORT'] = 16943  # Specify the port number

mysql = MySQL(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM customers WHERE customer_email=%s AND password=%s", (email, password))
    customer = cursor.fetchone()
    
    if customer:
        cursor.execute("SELECT * FROM clients WHERE client_id=%s", (customer['client_id'],))
        client = cursor.fetchone()
        return jsonify({'status': 'success', 'client': client, 'customer': customer})
    
    return jsonify({'status': 'failure', 'message': 'Invalid credentials'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
