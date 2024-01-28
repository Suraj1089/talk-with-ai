import openai
from functions.database import get_recent_messages
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
    

def get_chat_response(message_input):
    messages = get_recent_messages()
    print(messages)
    user_message = {"role": "user", "content": message_input}
    messages.append(user_message)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        print(response)
        message_txt = response["choices"][0]["message"]["content"]
        return message_txt
    except Exception as e:
        print(e)
        return str(e)