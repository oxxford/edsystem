from gtts import gTTS
import uuid


def get_speech(text):
    tts = gTTS(text=text, lang='en')
    filename = uuid.uuid4().hex + '.mp3'
    tts.save('./audio/' + filename)
    return filename


def get_my_ip():
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip
