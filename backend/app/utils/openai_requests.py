import openai
from app.internal.config import get_settings
from app.utils.database import get_recent_messages

openai.organization = get_settings().OPENAI_ORG
openai.api_key = get_settings().OPENAI_API_KEY


# Open AI - Whisper
# Convert audio to text
def convert_audio_to_text(audio_file):
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        message_text = transcript["text"]
        return message_text
    except Exception as e:
        return e

# Open AI - Chat GPT
# Convert audio to text


def get_chat_response(message_input):

    messages = get_recent_messages()
    user_message = {"role": "user", "content": message_input +
                    """Only say two or 3 words in Spanish if speaking in Spanish.
                      The remaining words should be in English"""}
    messages.append(user_message)
    print(messages)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        message_text = response["choices"][0]["message"]["content"]
        return message_text
    except Exception as e:
        return e
