from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from Python and FastAPI!"}


@app.get("/health")
def health():
    return {"status": "ok"}
