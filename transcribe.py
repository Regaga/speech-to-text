# Imports the Google Cloud client lii
from google.cloud import speech
import conver
def speech_to_text():
    client = speech.SpeechClient(bytes_1=None)
    #gcs_uri = "gs://my-audio-bucket-try/audiofromtg.flac"
    print('check1')
    bytes = conveconvert_to_pcm16b16000r(in_bytes=bytes)
    audio = speech.RecognitionAudio(content=bytes)
    config = speech.RecognitionConfig(
        encoding='LINEAR16',
        sample_rate_hertz=16000,
        language_code="ru-RU",
    )
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(result)
