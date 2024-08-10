from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Configuración de la conexión a la base de datos
conn = psycopg2.connect(
    dbname="ApiLogs",
    user="postgres",
    password="246494",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Lista de tokens válidos (como contraseñas) que identifican los servicios
VALID_TOKENS = {
    "service-1-token": "Servicio1",
    "service-2-token": "Servicio2",
    "service-3-token": "Servicio3",  
}

# Ruta para recibir los logs (registros de eventos)
@app.route('/logs', methods=['POST'])
def receive_log():
    # Verifica si hay un token en la solicitud y si es válido
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Token no proporcionado"}), 401

    token = auth_header.split(" ")[1]
    if token not in VALID_TOKENS:
        return jsonify({"error": "Token no válido"}), 403

    # Obtener el log enviado y guardarlo en la base de datos
    log = request.json
    if not log:
        return jsonify({"error": "Log no proporcionado o no es un JSON válido"}), 400

    received_at = datetime.now()  # Fecha y hora actuales (como objeto datetime)
    
    query = """
        INSERT INTO logs (timestamp, service_name, log_level, message, received_at)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        log['timestamp'],           # Cuándo ocurrió el evento
        log['service_name'],        # Qué servicio envió el log
        log['log_level'],           # Nivel de importancia del log (INFO, WARNING, ERROR)
        log['message'],             # Mensaje del log
        received_at                 # Cuándo se recibió el log en el servidor
    ))
    conn.commit()  # Guarda los cambios en la base de datos

    return jsonify({"message": "Log recibido y almacenado"}), 200

# Inicia el servidor en modo depuración
if __name__ == '__main__':
    app.run(debug=True,port=5000)