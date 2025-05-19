from flask import Flask, request, jsonify
import subprocess
import os
import tempfile

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract_metadata():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
        file.save(temp.name)

    try:
        result = subprocess.run(
            ["exiftool", "-j", temp.name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        metadata = result.stdout.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "ExifTool error", "details": e.stderr.decode("utf-8")}), 500
    finally:
        os.remove(temp.name)

    return metadata, 200
