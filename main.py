import telebot
import requests
from google.cloud import speech
import subprocess
import tempfile
import os


def convert_to_pcm16b16000r(in_filename=None, in_bytes=None):
    with tempfile.TemporaryFile() as temp_out_file:
        temp_in_file = None
        if in_bytes:
            temp_in_file = tempfile.NamedTemporaryFile(delete=False)
            temp_in_file.write(in_bytes)
            in_filename = temp_in_file.name
            temp_in_file.close()
        if not in_filename:
            raise Exception('Neither input file name nor input bytes is specified.')

        # Запрос в командную строку для обращения к FFmpeg
        command = [
            'ffmpeg',  # путь до ffmpeg.exe
            '-i', in_filename,
            '-f', 's16le',
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-'
        ]

        proc = subprocess.Popen(command, stdout=temp_out_file, stderr=subprocess.DEVNULL)
        proc.wait()

        if temp_in_file:
            os.remove(in_filename)

        temp_out_file.seek(0)
        return temp_out_file.read()


def speech_to_text(bytes=None):
    client = speech.SpeechClient()
    # gcs_uri = "gs://my-audio-bucket-try/audiofromtg.flac"
    bytes = convert_to_pcm16b16000r(in_bytes=bytes)
    audio = speech.RecognitionAudio(content=bytes)
    config = speech.RecognitionConfig(
        encoding='LINEAR16',
        sample_rate_hertz=16000,
        language_code="ru-RU",
    )
    response = client.recognize(config=config, audio=audio)
    return (response.results)


token=os.environ["TOKEN"]
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['voice'])
def send_answer(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    for result in speech_to_text(file.content):
        bot.send_message(message.chat.id, format(result.alternatives[0].transcript),reply_to_message_id=message.message_id)


if __name__ == '__main__':
    bot.polling(none_stop=True)
