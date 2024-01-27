import openai
from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from functions.openai_requests import convert_audio_to_text

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://localhost:4173",
    "http://localhost:4174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get('/health')
def hello():
    return {'data': 'hello'}

@app.post('/post-audio')
async def post_audio(file: UploadFile = File(...)):
    print(file) 

@app.get('/post-audio-get')
async def get_audio():
    # get saved audio
    with open('voice.mp3', "rb") as audio_file:
        message_decoded = convert_audio_to_text(audio_file)
        print(message_decoded)
    return "done"