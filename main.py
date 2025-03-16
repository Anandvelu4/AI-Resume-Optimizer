from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import fitz  # PyMuPDF for PDF Processing
import docx  # python-docx for Word file Processing

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the PDF and Word File Processor API"

# Configuring the upload folder
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check the file extension
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text from PDF or DOCX
def extract_text_from_resume(file_path):
    ext = os.path.splitext(file_path)[1][1:].lower()  # More reliable extension extraction
    text = ""

    if ext == "pdf":
        with fitz.open(file_path) as doc:
            text = "\n".join([page.get_text("text") for page in doc])
    elif ext == "docx":
        doc_obj = docx.Document(file_path)
        text = "\n".join([para.text for para in doc_obj.paragraphs])

    return text

# Route to upload and process resumes
@app.route("/upload", methods=["POST"])
def upload_resume():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
      return jsonify({"error": "No Selected File"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        extracted_text = extract_text_from_resume(file_path)

        return jsonify({"message": "Resume processed successfully", "text": extracted_text})

    return jsonify({"error": "Invalid file"}), 400

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

# Test fitz
from pymupdf import fitz
print(fitz.__doc__)

      


