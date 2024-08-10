import requests
import json
import time
import random
from datetime import datetime

# Definimos los servicios con su "llave" (token) y nombre
SERVICES = [
    {"token": "service-1-token", "name": "Servicio1"},
    {"token": "service-2-token", "name": "Servicio2"},
    {"token": "service-3-token", "name": "Servicio3"},
]

# URL del servidor que recibe los logs
LOG_SERVER_URL = "http://localhost:5000/logs"
# Diferentes niveles de importancia para los logs
LOG_LEVELS = ["INFO", "WARNING", "ERROR"]

# Función que envía un log
def send_log(service):
    # Elegimos al azar un nivel de log (INFO, WARNING, ERROR)
    log_level = random.choice(LOG_LEVELS)
    
    # Creamos el log con la información
    log = {
        "timestamp": datetime.now().isoformat(),  # Fecha y hora actuales
        "service_name": service['name'],  # Nombre del servicio
        "log_level": log_level,  # Nivel del log
        "message": f"Este es un log de {service['name']} con nivel {log_level}"  # Mensaje del log
    }
    
    # Encabezado con la "llave" (token) para autorización
    headers = {"Authorization": f"Bearer {service['token']}"}
    
    try:
        # Enviamos el log al servidor
        response = requests.post(LOG_SERVER_URL, json=log, headers=headers)
        response.raise_for_status()  # Esto lanzará un error para códigos de estado 4xx/5xx

        try:
            # Intentamos decodificar la respuesta JSON
            response_data = response.json()
            print(f"Enviado log: {response.status_code} - {response_data}")
        except json.JSONDecodeError:
            print(f"Enviado log: {response.status_code} - Respuesta no es un JSON válido.")

    except requests.exceptions.RequestException as e:
        # Capturamos cualquier error de red o de la petición
        print(f"Error al enviar el log: {e}")

# Programa principal
if __name__ == "__main__":
    while True:
        for service in SERVICES:
            send_log(service)  # Enviamos un log para cada servicio
            time.sleep(5)  # Esperamos 5 segundos antes de enviar el siguiente log
