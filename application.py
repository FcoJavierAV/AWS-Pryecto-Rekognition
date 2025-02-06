from http.client import responses
import boto3, os, base64
from flask import Flask, request, Response, abort, jsonify
from dotenv import load_dotenv
from processText import process_texts
from detectText import detect_text

load_dotenv()

accessKeyId = os.environ.get('ACCESS_KEY_ID')
secretKey = os.environ.get('ACCESS_SECRET_KEY')
bucketSource = os.environ.get('BUCKET_SOURCE')
region = os.environ.get('REGION')

if not all([accessKeyId, secretKey, bucketSource]):
    raise EnvironmentError("Faltan variables de entorno requeridas.")

application = Flask(__name__)

s3 = boto3.Session(
    aws_access_key_id=accessKeyId,
    aws_secret_access_key=secretKey,
    region_name=region
).resource('s3')

@application.route('/api/detectGames', methods=['POST'])
def detect_games():
    data = request.get_json()
    image = data.get('key')
    if not image:
        abort(400, description="Falta la clave 'key' en la solicitud.")

    try:
        detected_texts = detect_text(image)
        if not detected_texts:
            return jsonify({'error': 'No se detectó texto o hubo un error en Rekognition'}), 400

        games_data = process_texts(detected_texts)
    except Exception as error:
        print(error)
        abort(500, description="Error procesando los textos.")

    return jsonify({'message': 'Juegos detectados exitosamente', 'data': games_data})

if __name__ == "__main__":
    application.debug = True
    application.run()
