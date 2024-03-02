import boto3
from contextlib import closing
from datetime import datetime

class PollyService:
    def __init__(self):
        self.client = boto3.client('polly')

    def synthesize_speech(self, text, output_format = 'mp3', voice_id = 'Joanna'):
        response = self.client.synthesize_speech(
            Text = text,
            OutputFormat = output_format,
            VoiceId = voice_id
        )

        # Save the audio to a file
        with closing(response['AudioStream']) as stream:
            output_file = f'audio_files/translated_speech_{datetime.now().strftime("%Y%m%d_%H%M%S")}.{output_format}'
            with open(output_file, 'wb') as file:
                file.write(stream.read())
        
        return output_file
