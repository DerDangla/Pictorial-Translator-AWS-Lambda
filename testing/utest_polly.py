import os, sys
import unittest

import polly_service

class PollyServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = PollyServiceTest.PollyService()

    def test_synthesize_speech(self):
        text_to_speech = self.service.synthesize_speech('My name is Emander', 'mp3', 'Joanna')
        self.assertTrue(text_to_speech)
        self.assertEqual('mp3', text_to_speech['output_format'])
        self.assertEqual('Joanna', text_to_speech['voice_id'])
        print('OK test for text_to_speech')
        

if __name__ == "__main__":
    unittest.main()
