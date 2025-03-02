from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Ensure static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Serve `index.html` when the user visits the root URL
@app.get("/")
async def serve_homepage():
    return FileResponse("static/index.html")
