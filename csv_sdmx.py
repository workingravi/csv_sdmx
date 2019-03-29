import os, sys
from flask import Flask, render_template, request, redirect, flash, url_for, render_template_string, session
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['csv', 'pdf',])
UPLOAD_FOLDER = './static'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '314159'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/upload', methods=['GET','POST'])
def handle_upload():

    # check if the post request has the file part
    if 'file' not in request.files:
        session.pop('_flashes', None)
        flash('No file part - Pls try again')
        return redirect(url_for('main'))
    else:
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            session.pop('_flashes', None)
            flash('No selected file...Pls try again')
            return redirect(url_for('main'))
        if not allowed_file(file.filename):
            session.pop('_flashes', None)
            flash("This file extension is not supported. Pls try again.")
            return redirect(url_for('main'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("upload.html", filename=filename)

if __name__ == "__main__":
    app.run(debug=True)





