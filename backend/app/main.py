
from fastapi import File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.apis import users
from app.internal.server import app
from app.utils.database import store_messages
from app.utils.openai_requests import convert_audio_to_text, get_chat_response
from app.utils.text_to_speech import convert_text_to_speech

app.include_router(users.router)


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
