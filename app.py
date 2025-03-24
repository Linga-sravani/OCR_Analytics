from flask import Flask, render_template, request, url_for
import os
from ocr_script import read_text_from_image

app = Flask(__name__, static_folder="static")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded"
        file = request.files["file"]
        if file.filename == "":
            return "No file selected"
        
        # Save the uploaded file
        file_path = os.path.join(app.static_folder, file.filename)
        file.save(file_path)
        
        # Extract text using OCR
        extracted_text = read_text_from_image(file_path)
        
        # Generate the URL for the static file
        image_url = url_for('static', filename=file.filename)
        
        # Render the template with extracted text and image URL
        return render_template(
            "index.html",
            extracted_text=extracted_text,
            image_url=image_url
        )
    
    return render_template("index.html", extracted_text=None, image_url=None)

if __name__ == "__main__":
    app.run(debug=True)