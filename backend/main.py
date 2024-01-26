from fastapi import FastAPI, Depends

app = FastAPI()


@app.get('/')
def hello():
    return {'data': 'hello'}