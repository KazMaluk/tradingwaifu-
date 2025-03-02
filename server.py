from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Ensure the static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

# Serve static files (frontend assets)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Serve `index.html` when users visit the root URL
@app.get("/")
async def serve_homepage():
    return FileResponse("static/index.html")
