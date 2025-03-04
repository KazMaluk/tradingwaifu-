from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="static")

# Serve `index.html` at root `/`
@app.route("/")
def serve_home():
    return send_from_directory("static", "index.html")

# Serve static files (CSS, JS, Images)
@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
