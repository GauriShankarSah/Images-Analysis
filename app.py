from flask import Flask, request, jsonify, render_template_string
import os
from search import search_image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ✅ Simple HTML UI
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Similarity Search</title>
</head>
<body>
    <h2>Upload an Image 🔍</h2>
    
    <form action="/search" method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Search</button>
    </form>

    {% if results %}
        <h3>Results:</h3>
        <ul>
        {% for r in results %}
            <li>
                {{ r.image }} - Score: {{ "%.4f"|format(r.score) }}
            </li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE)


@app.route("/search", methods=["POST"])
def search():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    results = search_image(path)

    # Convert to dict format for template
    formatted = [{"image": img, "score": score} for img, score in results]

    return render_template_string(HTML_PAGE, results=formatted)


# Optional API (for curl/Postman)
@app.route("/api/search", methods=["POST"])
def api_search():
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
