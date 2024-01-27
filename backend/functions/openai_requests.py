import openai

from decouple import config


openai.organization = config("OPENAI_ORG")
openai.api_key = config("OPENAI_API_KEY")

# OpenAi whisper

def convert_audio_to_text(audio_file):
    try: 
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        message = transcript['text']
        return message 
    except Exception as e:
        print(e)
        return