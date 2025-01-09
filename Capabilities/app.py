from flask import Flask, request, jsonify
from flask_cors import CORS
from chalicelib import storage_service, recognition_service, translation_service, polly_service
import base64

app = Flask(__name__)

CORS(app)

# Initialize servicess
storage_location = 'pic-translate-store'
storage_service = storage_service.StorageService(storage_location)
recognition_service = recognition_service.RecognitionService(storage_service)
translation_service = translation_service.TranslationService()
polly_service = polly_service.PollyService()

# Health check endpoint
@app.route('/validate', methods=['GET'])
def validate_api():
    """Simple endpoint to validate that the API is running."""
    return jsonify({"status": "success", "message": "API is running successfully!"})

# Upload image endpoint
@app.route('/images', methods=['POST'])
def upload_image():
    """Processes file upload and saves file to storage service"""
    data = request.get_json()
    file_name = data['filename']
    file_bytes = base64.b64decode(data['filebytes'])

    image_info = storage_service.upload_file(file_bytes, file_name)
    return jsonify(image_info)

# Translate text in image
@app.route('/images/<image_id>/translate-text', methods=['POST'])
def translate_image_text(image_id):
    """Detects then translates text in the specified image"""
    data = request.get_json()
    from_lang = data['fromLang']
    to_lang = data['toLang']
    MIN_CONFIDENCE = 80.0

    text_lines = recognition_service.detect_text(image_id)
    translated_lines = []

    for line in text_lines:
        if float(line['confidence']) >= MIN_CONFIDENCE:
            translated_line = translation_service.translate_text(line['text'], from_lang, to_lang)
            translated_lines.append({
                'text': line['text'],
                'translation': translated_line['translatedText'],
                'boundingBox': line['boundingBox']
            })

    return jsonify(translated_lines)

# Text-to-speech endpoint
@app.route('/text-to-speech', methods=['POST'])
def create_speech():
    """Converts text to speech and saves the audio"""
    data = request.get_json()
    combined_translated_text = data['combined_translated_text']
    output_file = polly_service.synthesize_speech(' '.join(combined_translated_text))
    return jsonify({"outputFile": output_file})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
