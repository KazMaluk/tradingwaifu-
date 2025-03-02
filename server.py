from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Ensure the static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

# Serve static files (this serves `index.html` properly)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
