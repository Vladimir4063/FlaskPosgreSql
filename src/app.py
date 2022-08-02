from flask import Flask, request, jsonify
from psycopg2 import connect, extras
from cryptography.fernet import Fernet

app = Flask(__name__)

# cifrar contraseña 
key = Fernet.generate_key()

# connect
host = 'localhost'
port = 5432
dbname = 'usersdb'
user = 'postgres'
password = 'admin'

def get_connection():
    conn = connect(host = host, port = port, dbname = dbname, user = user, password = password)
    return conn

# Start
@app.get('/')
def home():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT 1 + 1")
    result = cur.fetchone()
    print(result)
    return 'Hello Word'
# End

@app.get('/api/users')
def get_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(users)

@app.post('/api/users')
def create_user():
    new_user = request.get_json() 
    username = new_user['username']
    email = new_user['email']
    # encripto psw
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))
    print(username, email, password)

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor) # RealDictCursor convierte la respuesta en tuplas

    # genero una consulta con variables
    cur.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING *',
                (username, email, password))
    
    new_created_user = cur.fetchone()
    print(new_created_user)

    conn.commit()  
    cur.close()
    conn.close()

    return jsonify(new_created_user)

@app.delete('/api/users/<id>')
def delete_user(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    
    # elimino user
    cur.execute('DELETE FROM users WHERE id = %s',(id,))
    conn.commit()
    
    # traigo nuevamente los usuarios
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    conn.close()
    cur.close()

    return jsonify(users)

@app.put('/api/users/1')
def update_user():
    return 'updatting users'

@app.get('/api/users/<id>')
def get_user(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM users WHERE id = %s',(id,))
    user = cur.fetchone()
    
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)