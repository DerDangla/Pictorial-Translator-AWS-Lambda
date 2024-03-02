import boto3
from contextlib import closing

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
            output_file = 'translated_speech.mp3'
            with open(output_file, 'wb') as file:
                file.write(stream.read())
        
        return output_file
