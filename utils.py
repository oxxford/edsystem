from gtts import gTTS
import uuid


def get_speech(text):
    tts = gTTS(text=text, lang='en')
    filename = uuid.uuid4().hex + '.mp3'
    tts.save('./audio/' + filename)
    return filename
