import logging
import boto3


class TranslationService:
    def __init__(self):
        self.client = boto3.client('translate')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def translate_text(self, text, source_language='auto', target_language='en'):
        try:
            self.logger.info(f"Translating text: {text[:50]}...")  # Log the first 50 characters
            self.logger.info(f"Source: {source_language}, Target: {target_language}")
            
            response = self.client.translate_text(
                Text=text,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language
            )

            self.logger.info(f"Translation response: {response}")

            translation = {
                'translatedText': response['TranslatedText'],
                'sourceLanguage': response['SourceLanguageCode'],
                'targetLanguage': response['TargetLanguageCode']
            }
            return translation
        except Exception as e:
            self.logger.error(f"Error during translation: {e}")
            raise
