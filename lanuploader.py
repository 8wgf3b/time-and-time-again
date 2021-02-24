from flask import Flask, abort, render_template, request, redirect,url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = './temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


upload_html = """
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form action='' method="POST" enctype="multipart/form-data">
    <p><input type='file' name='file[]' multiple=''>
        <input type='submit' value='upload'>
    </p>

</form>"""


@app.route('/upload/',methods = ['GET','POST'])
def upload_file():
    if request.method =='POST':
        files = request.files.getlist('file[]')
        saved = ''
        for file in files:
            filename = secure_filename(file.filename)
            saved += filename + "<br/>"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return f'Done uploading <br/>{saved}<br/><br/> <a href="../upload">upload more</a>'
    return upload_html


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')

