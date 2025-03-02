from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Ensure the static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

# Serve `index.html` from the `static/` directory
app.mount("/", StaticFiles(directory="static", html=True), name="static")
