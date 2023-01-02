from flask import Flask, request, jsonify, send_file
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
    conn = connect(host=host, port=port, dbname=dbname,
                   user=user, password=password)
    return conn

# Start
# @app.get('/')
# def home():
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT 1 + 1")
#     result = cur.fetchone()
#     print(result)
#     return 'Hello Word'
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
    # RealDictCursor convierte la respuesta en tuplas/filas
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

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
    cur.execute('DELETE FROM users WHERE id = %s RETURNING * ', (id,))

    # traigo el usuario eliminado
    user = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if user is None:
        return jsonify({"message": "User not found"}), 404
    print(user)
    return jsonify(user)


@app.put('/api/users/<id>')
def update_user(id):

    conn = get_connection()
    # RealDictCursor convierte la respuesta en tuplas/filas
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8')) # Encripto contraseña

    cur.execute(
        'UPDATE users SET username=%s, email = %s, password = %s WHERE id = %s RETURNING *', (username, email, password, id)
        )
    update_user = cur.fetchone()
    conn.commit()
    print(update_user)

    cur.close()
    conn.close()
    if update_user is None:
        return jsonify({'message': 'User not found'}), 404

    print(update_user)
    return jsonify(update_user)


@app.get('/api/users/<id>')
def get_user(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cur.fetchone()

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user)

@app.get('/')
def home():
    return send_file('static/index.html')


if __name__ == '__main__':
    app.run(debug=True)
