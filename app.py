from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)

CORS(app) 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api-test")
def api_test_page():
    return render_template("api_test.html")

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "message": "API is working!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

