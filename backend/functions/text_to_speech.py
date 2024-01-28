import requests

from decouple import config

ELEVEN_LABS_API_KEY = config('ELEVEN_LABS_API_KEY')

# convert text to speech
def convert_text_to_speech(message):
    body = {
        "text": message,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
    }

    # voice to use 
    voice_id = "21m00Tcm4TlvDq8ikWAM"

    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": 'application/json',
        "accept": "audio/mpeg"
    }

    endpoint = f"https://api.elevenlabs.io/v1/test-to-speech/{voice_id}"

    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        print(e)
        return e 
    
    if response.status_code == 200:
        return response.content
    else:
        return "Error"