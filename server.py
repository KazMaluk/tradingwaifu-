from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files (frontend)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
