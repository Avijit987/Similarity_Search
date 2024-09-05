from flask import Flask, render_template, request, redirect, url_for
import os
from search import find_similar_images

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Perform similarity search
        results = find_similar_images(file_path, app.config['UPLOAD_FOLDER'])
        return render_template('results.html', results=results, uploaded_image=file.filename)

if __name__ == '__main__':
    app.run(debug=True)
