import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA = "menu_pizzas.db"

#-----------------------------------
# Conexión a la base de datos SQLite
def conectar():
    conn = sqlite3.connect(DATA)
#    conn.row_factory = sqlite3.Row
    return conn
#-----------------------------------

# Creación de la tabla 'pizzas' si no existe
conn = conectar()
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS pizzas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            precio REAL,
            detalles TEXT,
            imagen TEXT
          )''')
conn.commit()
c.close()
conn.close()

@app.route('/api/pizzas', methods=['GET'])
def obtener_pizzas():
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM pizzas')
    pizzas = []
    for row in c.fetchall():
        pizza = {
            'id': row[0],
            'nombre': row[1],
            'precio': row[2],
            'detalles': row[3],
            'imagen': row[4]
        }
        pizzas.append(pizza)
    c.close()
    conn.close()
    return jsonify(pizzas)

@app.route('/api/pizzas', methods=['POST'])
def crear_pizza():
    conn = conectar()
    c = conn.cursor()
    nueva_pizza = request.get_json()
    nombre = nueva_pizza['nombre']
    precio = nueva_pizza['precio']
    detalles = nueva_pizza['detalles']
    imagen = nueva_pizza['imagen']

    c.execute("INSERT INTO pizzas (nombre, precio, detalles, imagen) VALUES (?, ?, ?, ?)",
              (nombre, precio, detalles, imagen))
    conn.commit()
    c.close()
    conn.close()
    return jsonify({'mensaje': 'Pizza creada correctamente'})

@app.route('/api/pizzas/<int:pizza_id>', methods=['DELETE'])
def borrar_pizza(pizza_id):
    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM pizzas WHERE id=?", (pizza_id,))
    conn.commit()
    c.close()
    conn.close()
    return jsonify({'mensaje': 'Pizza borrada correctamente'})

@app.route('/api/pizzas/<int:pizza_id>', methods=['PUT'])
def modificar_pizza(pizza_id):
    conn = conectar()
    c = conn.cursor()
    pizza_modificada = request.get_json()
    nuevo_nombre = pizza_modificada['nombre']
    nuevo_precio = pizza_modificada['precio']
    nuevos_detalles = pizza_modificada['detalles']
    nueva_imagen = pizza_modificada['imagen']

    c.execute("UPDATE pizzas SET nombre=?, precio=?, detalles=?, imagen=? WHERE id=?",
              (nuevo_nombre, nuevo_precio, nuevos_detalles, nueva_imagen, pizza_id))
    conn.commit()
    c.close()
    conn.close()
    return jsonify({'mensaje': 'Pizza modificada correctamente'})

if __name__ == '__main__':
    app.run()
