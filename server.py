from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Resolve absolute path to static folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Serve index.html at root
@app.get("/", response_class=FileResponse)
async def serve_homepage():
    file_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(file_path):
        return {"detail": f"File not found at {file_path}"}
    return FileResponse(file_path, media_type="text/html")
