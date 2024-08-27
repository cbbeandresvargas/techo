from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/send_data', methods=['POST'])
def send_data():
    # Obtener los datos del cuerpo de la solicitud
    data = request.get_json()
    id_area = data.get('id_area')
    id_sensor = data.get('id_sensor')
    humedad = data.get('humedad')
    consumo = data.get('consumo')

    # Validar los datos
    if not (id_area and id_sensor and humedad is not None and consumo is not None):
        return jsonify({'error': 'Faltan parámetros requeridos'}), 400

    # Preparar los datos para enviar
    payload = {
        'id_area': id_area,
        'id_sensor': id_sensor,
        'humedad': humedad,
        'consumo': consumo
    }

    # Hacer la llamada POST a la API externa
    try:
        response = requests.post('https://smartriego.pockethost.io/api/collections/estadisticas/records', json=payload)
        response.raise_for_status()  # Lanza un error si la solicitud falla
        
        # Obtener el JSON de la respuesta
        response_data = response.json()
        
        # Extraer el ID de la respuesta
        record_id = response_data.get('id', None)
        
        # Construir la respuesta de la API
        return jsonify({'success': True, 'id': record_id}), 200

    except requests.RequestException:
        return jsonify({'error': 'Error al enviar los datos'}), 500

if __name__ == '__main__':
    app.run(debug=True)



# curl -X POST http://127.0.0.1:5000/api/send_data -H "Content-Type: application/json" -d '{"id_area": "area1", "id_sensor": "sensor1", "humedad": 75.5, "consumo": 123.4}'



#virtualenv techo
#cd scripts
#.\activate
#cd ..
#pip install flask requests
#code .