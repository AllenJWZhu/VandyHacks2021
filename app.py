# app.py
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import imageProcess

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/encryptImage', methods=['GET', 'POST'])
def encrypt_image():
    imageProcess.encrypt_to_disc('img/space.jpg')
    return render_template('index.html', filename="the_golden_disc.png")


@app.route('/decryptImage', methods=['GET', 'POST'])
def decrypt_image():
    imageProcess.decrypt_to_picture('static/uploads/the_golden_disc.png', 'static/uploads/decryptedPic.png')
    return render_template('index.html', filename="decryptedPic.png")


@app.route('/uploadImage', methods=['GET', 'POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


#     # app.route('/changeImage', methods = ['GET', 'POST'])
#     # def change_image(fileName):
#     # Get file here 
#     # filename = secure_filename(file.filename)
#     # image = file.get(os.path.join(app.config['UPLOAD_FOLDER'], filename))


#     # encrypt the image here
#     # encryptedFile = encryptImage(image)

#     # save again, get the encrypted file name
#     # encryptedFilename = 
#     # follow logic to render encrypted
#     return render_template('encrypted.html', filename=encryptedFilename)


@app.route('/')
def home():
    return render_template('create_account.html')


@app.route('/index', methods=['GET', 'POST'])
def image():
    return render_template('index.html', upload_image=upload_image)


@app.route('/index', methods=['GET', 'POST'])
def encryptIMG():
    return render_template('index.html', encrypt_image=encrypt_image)

@app.route('/index', methods=['GET', 'POST'])
def decryptIMG():
    return render_template('index.html', decrypt_image=decrypt_image)


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run(debug=True)
