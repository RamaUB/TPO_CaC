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

c.execute('''CREATE TABLE IF NOT EXISTS carrito(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            precio REAL,
            cantidad REAL,
            imagen TEXT
          )''')

c.execute('''CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_pedido INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL,
            imagen TEXT NOT NULL
          )''')

conn.commit()  
c.close()
conn.close()

#----------------------------------------------------
# Seccion MENU
#----------------------------------------------------

@app.route('/api/pizzas', methods=['GET'])
def obtener_pizzas():
    try:
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
        return jsonify(pizzas)
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500
    finally:
        c.close()
        conn.close()

@app.route('/api/pizzas', methods=['POST'])
def crear_pizza():
    try:
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
        return jsonify({'mensaje': 'Pizza creada correctamente'})
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500
    finally:
        c.close()
        conn.close()

@app.route('/api/pizzas/<int:pizza_id>', methods=['DELETE'])
def borrar_pizza(pizza_id):
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute("DELETE FROM pizzas WHERE id=?", (pizza_id,))
        conn.commit()
        return jsonify({'mensaje': 'Pizza borrada correctamente'})
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500
    finally:
        c.close()
        conn.close()

@app.route('/api/pizzas/<int:pizza_id>', methods=['PUT'])
def modificar_pizza(pizza_id):
    try:
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
        return jsonify({'mensaje': 'Pizza modificada correctamente'})
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500
    finally:
        c.close()
        conn.close()

#------------------------------------------------------------------
#Seccion de carrito
#------------------------------------------------------------------

@app.route('/api/carrito', methods=['GET'])
def obtener_productos():
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute('SELECT * FROM carrito')
        carrito = []
        for row in c.fetchall():
            carrit = {
                'id': row[0],
                'nombre': row[1],
                'precio': row[2],
                'cantidad': row[3],
                'imagen': row[4]
            }
            carrito.append(carrit)
        return jsonify(carrito)
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500
    finally:
        c.close()
        conn.close()

@app.route('/api/carrito', methods=['POST'])
def agregar_carrito():
    try:
        conn = conectar()
        c = conn.cursor()
        nuevo_producto = request.get_json()
        nombre = nuevo_producto['nombre']
        precio = nuevo_producto['precio']
        cantidad = nuevo_producto['cantidad']
        imagen = nuevo_producto['imagen']

        c.execute("INSERT INTO carrito (nombre, precio, cantidad, imagen) VALUES (?, ?, ?, ?)",
                  (nombre, precio, cantidad, imagen))
        conn.commit()
        return jsonify({'mensaje': 'Pizza creada correctamente'})
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500
    finally:
        c.close()
        conn.close()

@app.route('/api/carrito/<int:producto_id>', methods=['DELETE'])
def borrar_producto(producto_id):
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute("DELETE FROM carrito WHERE id=?", (producto_id,))
        conn.commit()
        return jsonify({'mensaje': 'Pizza borrada correctamente'})
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500
    finally:
        c.close()
        conn.close()

@app.route('/api/carrito/<int:producto_id>', methods=['PUT'])
def modificar_producto(producto_id):
    try:
        conn = conectar()
        c = conn.cursor()
        producto_modificado = request.get_json()
        nuevo_nombre = producto_modificado['nombre']
        nuevo_precio = producto_modificado['precio']
        nueva_cantidad = producto_modificado['cantidad']
        nueva_imagen = producto_modificado['imagen']

        c.execute("UPDATE carrito SET nombre=?, precio=?, cantidad=?, imagen=? WHERE id=?",
                  (nuevo_nombre, nuevo_precio, nueva_cantidad, nueva_imagen, producto_id))
        conn.commit()
        return jsonify({'mensaje': 'Pizza modificada correctamente'})
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500
    finally:
        c.close()
        conn.close()

#----------------------------------------------------------------------------------------
#Seccion de pedidos
#----------------------------------------------------------------------------------------

@app.route('/api/pedidos', methods=['GET'])
def obtener_pedidos():
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute('SELECT * FROM pedidos')
        pedidos = []
        for row in c.fetchall():
            pedido = {
                'id': row[0],
                'numero_pedido': row[1],
                'nombre': row[2],
                'precio': row[3],
                'cantidad': row[4],
                'imagen': row[5]
            }
            pedidos.append(pedido)
        return jsonify(pedidos), 200
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500
    finally:
        c.close()
        conn.close()

@app.route('/api/pedidos', methods=['POST'])
def guardar_pedido():
    try:
        conn = conectar()
        c = conn.cursor()

        pedidos = request.get_json()

        # Obtener el último número de pedido generado
        c.execute('SELECT MAX(numero_pedido) FROM pedidos')
        resultado = c.fetchone()
        ultimo_numero_pedido = resultado[0] or 0
        nuevo_numero_pedido = ultimo_numero_pedido + 1

        for pedido in pedidos:
            nombre = pedido['nombre']
            precio = pedido['precio']
            cantidad = pedido['cantidad']
            imagen = pedido['imagen']

            c.execute('INSERT INTO pedidos (numero_pedido, nombre, precio, cantidad, imagen) VALUES (?, ?, ?, ?, ?)',
                      (nuevo_numero_pedido, nombre, precio, cantidad, imagen))
        
        # Eliminar los datos de la tabla carrito
        c.execute('DELETE FROM carrito')
        
        conn.commit()
        return jsonify({'mensaje': 'Pedidos guardados correctamente'}), 201
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500
    finally:
        c.close()
        conn.close()



@app.route('/api/pedidos/<int:numero_pedido>', methods=['DELETE'])
def eliminar_pedido(numero_pedido):
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute('DELETE FROM pedidos WHERE numero_pedido = ?', (numero_pedido,))
        conn.commit()
        return jsonify({'mensaje': 'Pedidos eliminados correctamente'}), 200
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500
    finally:
        c.close()
        conn.close()

#-------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run()
