from fastapi import FastAPI

app = FastAPI(title="Window site")

@app.get("/")
def root():
    return {"message":"API is running"}