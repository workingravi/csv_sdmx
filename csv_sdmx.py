import os
from conv import conv
from flask import Flask, render_template, request, redirect, flash, url_for, send_file, session
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['csv',])
UPLOAD_FOLDER = os.path.dirname(__file__) + '/static'
op_filename = ""

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '314159'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def main():
    return render_template("convert.html")

@app.route('/download', methods=['GET','POST'])
def handle_download():
    op_filename = app.config['OUTPUT_FILE']
    if op_filename != "":
        return send_file(op_filename, as_attachment=True)


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
            csvfilename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(csvfilename)
            # generate the input and output filename with .xml extension
            file_firstname = filename.rsplit('.', 1)[0]
            opfilename = file_firstname + '.xml'
            opfilename =os.path.join(app.config['UPLOAD_FOLDER'], opfilename)
            app.config['OUTPUT_FILE'] = opfilename
            # call function to convert
            conv(csvfilename, opfilename)
            return render_template("upload.html", filename=filename)

if __name__ == "__main__":
    app.run(debug=True)



