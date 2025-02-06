import boto3
import os

bucketSource = os.environ.get('BUCKET_SOURCE')
region_name = os.environ.get('REGION')

def detect_text(image_url):
    rekognition_client = boto3.client('rekognition', region_name=region_name)

    try:
        response = rekognition_client.detect_text(
            Image={'S3Object': {'Bucket': bucketSource, 'Name': image_url}}
        )

        detected_text = response['TextDetections']
        return [text['DetectedText'] for text in detected_text if text['Type'] == 'LINE']
    except Exception as e:
        print(f"Error detecting text: {e}")
        return None
