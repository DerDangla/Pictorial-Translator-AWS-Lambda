import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class RecognitionService:
    def __init__(self, storage_service):
        self.client = boto3.client('rekognition')
        self.bucket_name = storage_service.get_storage_location()

    def detect_text(self, file_name):
        logger.info(f"DetectText called with Bucket: {self.bucket_name}, File: {file_name}")
        try:
            response = self.client.detect_text(
                Image={
                    'S3Object': {
                        'Bucket': self.bucket_name,
                        'Name': file_name
                    }
                }
            )
            logger.info(f"DetectText response: {response}")
        except Exception as e:
            logger.error(f"Error during DetectText: {e}")
            raise

        lines = []
        for detection in response['TextDetections']:
            if detection['Type'] == 'LINE':
                lines.append({
                    'text': detection['DetectedText'],
                    'confidence': detection['Confidence'],
                    'boundingBox': detection['Geometry']['BoundingBox']
                })

        return lines