from flask import Flask, request, jsonify, render_template_string
import os
from search import search_image, load_assets

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

loaded = False


HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Similarity Search</title>
</head>
<body>

    <h2>Step 1: Upload FAISS + PKL</h2>
    <form action="/load" method="post" enctype="multipart/form-data">
        <input type="file" name="faiss" accept=".faiss" required><br><br>
        <input type="file" name="pkl" accept=".pkl" required><br><br>
        <button type="submit">Load Model</button>
    </form>

    <hr>

    <h2>Step 2: Upload Query Image 🔍</h2>
    <form action="/search" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept="image/*" required>
        <button type="submit">Search</button>
    </form>

    {% if message %}
        <p>{{ message }}</p>
    {% endif %}

    {% if results %}
        <h3>Results:</h3>
        <ul>
        {% for r in results %}
            <li>{{ r.image }} - Score: {{ "%.4f"|format(r.score) }}</li>
        {% endfor %}
        </ul>
    {% endif %}

</body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE)


@app.route("/load", methods=["POST"])
def load():
    global loaded

    if "faiss" not in request.files or "pkl" not in request.files:
        return render_template_string(HTML_PAGE, message="❌ Upload both files")

    faiss_file = request.files["faiss"]
    pkl_file = request.files["pkl"]

    try:
        load_assets(faiss_file, pkl_file)
        loaded = True
        return render_template_string(HTML_PAGE, message="✅ Model loaded successfully!")
    except Exception as e:
        return render_template_string(HTML_PAGE, message=f"❌ Error: {str(e)}")


@app.route("/search", methods=["POST"])
def search():
    if not loaded:
        return render_template_string(HTML_PAGE, message="❌ Load FAISS + PKL first!")

    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    results = search_image(path)

    formatted = [{"image": img, "score": score} for img, score in results]

    return render_template_string(HTML_PAGE, results=formatted)


# Optional API
@app.route("/api/search", methods=["POST"])
def api_search():
    if not loaded:
        return jsonify({"error": "Load FAISS + PKL first"}), 400

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    results = search_image(path)

    return jsonify({
        "results": [
            {"image": img, "score": score}
            for img, score in results
        ]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
