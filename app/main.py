from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "RAG Knowledge Base API", "docs": "/docs"}
def health():
    return {"status": "ok"}