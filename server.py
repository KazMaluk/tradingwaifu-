from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

PORT = os.getenv("PORT", "8080")
print(f"Starting app on port: {PORT}")
print(f"Current working directory: {os.getcwd()}")

# Hardcode Railway’s expected path
STATIC_DIR = "/app/static"
print(f"Static folder exists: {os.path.exists(STATIC_DIR)}")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def serve_homepage():
    file_path = os.path.join(STATIC_DIR, "index.html")
    print(f"Looking for index.html at: {file_path}")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/html")
    return {"detail": f"File not found at {file_path}"}
