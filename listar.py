from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de la conexión a PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host="host.docker.internal",
        database="items",
        user="postgres",
        password="stalin"
    )

@app.route('/productos', methods=['GET'])
def listar_productos():
    """Listar todos los productos"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT id, name, description, price, stock, category_id FROM products;"
        cursor.execute(query)
        productos = cursor.fetchall()

        # Transformar los resultados en formato JSON
        productos_list = []
        for producto in productos:
            productos_list.append({
                'id': producto[0],
                'name': producto[1],
                'description': producto[2],
                'price': producto[3],
                'stock': producto[4],
                'category_id': producto[5]
            })

        return jsonify(productos_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Bloque __main__ para ejecutar el microservicio en el puerto 5002
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
