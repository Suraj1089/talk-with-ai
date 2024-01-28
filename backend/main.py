import openai
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from functions.database import reset_messages, store_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech

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

@app.get('/set')
def set():
    reset_messages()
    return {'message': 'conversation reset'}


@app.get('/reset')
def reset_conversation():
    reset_messages()
    return {'message': 'conversation reset'}


@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")
    message_decoded = convert_audio_to_text(audio_input)

    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")
    chat_response = get_chat_response(message_decoded)

    store_messages(message_decoded, chat_response)

    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed chat response")
    audio_output = convert_text_to_speech(chat_response)

    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed audio output")
    def iterfile():
        yield audio_output

    return StreamingResponse(iterfile(), media_type="application/octet-stream")
