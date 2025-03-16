from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import fitz #PyMuPDF for PDF Processing
import docx #python-docx for Word file Processing
from frontend import *

app=Flask(__name__)
@app.route('/')
def home():
    return "Welcome to the PDF and Word File Processor API"
#Configuring the upload folder
UPLOAD_FOLDER="uploads"
ALLOWED_EXTENSIONS={"pdf","docx"}
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#Function to check the file extension
def allowed_file(filename):
  return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

#Function to extract text from PDF
def extract_text_from_resume(file_path):
  ext=file_path.rsplit(".",1)[1].lower()
  if ext=="pdf":
    with fitz.open(file_path) as doc:
      text="\n".join([page.get_text("text") for page in doc])
  elif ext=="docx":
    doc=docx.Document(file_path)
    text="\n".join([para.text for para in doc.paragraphs])
  else:
    text=""
  return text

#Reoute to upload and process resumes
@app.route("/upload",methods=["POST"])
def upload_resume():
  if "file" not in request.files:
    return jsonify({"error":"No File provided"}),400
  file=request.files["file"]
  if file.filename=="":
    return jsonify({"error":"No selected file"}),400
  if file and allowed_file(file.filename):
    filename=secure_filename(file.filename)
    file_path=os.path.join(app.config["UPLOAD_FOLDER"],filename)
    file.save(file_path)
    extracted_text=extract_text_from_resume(file_path)
    return jsonify({"Message":"Resume processed Successfully", "text":extracted_text})
  return jsonify({"error":"Invalid File"}),400

# Run the Flask app
if __name__=="__main__":
  app.run(host='0.0.0.0', port=5000)


      


