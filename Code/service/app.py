import os
from flask import Flask, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

from get_captions import *

basedir = os.path.abspath(os.path.dirname(__file__))

static_foder = os.path.join('static', 'img')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')  # you'll need to create a folder named uploads
app.config['UPLOAD_FOLDER'] = static_foder

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

# for uploding file
class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])
    submit = SubmitField('Predict')


@app.route('/')
def home():
    model_image = os.path.join(app.config['UPLOAD_FOLDER'], 'model.PNG')
    return render_template('index.html', model_image=model_image)


@app.route('/index')
def index():
    model_image = os.path.join(app.config['UPLOAD_FOLDER'], 'model.PNG')
    return render_template('index.html', model_image=model_image)


@app.route('/predict', methods=['GET', 'POST'])
def predict():

    img_files = {
        "img1": os.path.join(app.config['UPLOAD_FOLDER'], 'bb.jpg'),
        "img2": os.path.join(app.config['UPLOAD_FOLDER'], 'a.jpg'),
        "img3": os.path.join(app.config['UPLOAD_FOLDER'], 'c.jpg'),
        "img4": os.path.join(app.config['UPLOAD_FOLDER'], 'd.jpg'),
    }

    # pred_image=None
    form = UploadForm()
    #form.submit.label.text = 'Predict'
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)

        print("this is file Name", filename)
        #predict_result = load_mode_and_predict("uploads/"+filename)
        predict_result = get_caption_prediction("uploads/" + filename)[0]
        pred_image = file_url
    else:
        predict_result = None
        pred_image = None
    return render_template('prediction.html', form=form, img_files=img_files, pred_image=pred_image, predict_result=predict_result)


if __name__ == '__main__':
    app.run()
import os
from flask import Flask, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

from get_captions import *

basedir = os.path.abspath(os.path.dirname(__file__))

static_foder = os.path.join('static', 'img')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')  # you'll need to create a folder named uploads
app.config['UPLOAD_FOLDER'] = static_foder

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])
    submit = SubmitField('Predict')


@app.route('/')
def home():
    model_image = os.path.join(app.config['UPLOAD_FOLDER'], 'model.PNG')
    return render_template('index.html', model_image=model_image)


@app.route('/index')
def index():
    model_image = os.path.join(app.config['UPLOAD_FOLDER'], 'model.PNG')
    return render_template('index.html', model_image=model_image)


@app.route('/predict', methods=['GET', 'POST'])
def predict():

    img_files = {
        "img1": os.path.join(app.config['UPLOAD_FOLDER'], 'bb.jpg'),
        "img2": os.path.join(app.config['UPLOAD_FOLDER'], 'a.jpg'),
        "img3": os.path.join(app.config['UPLOAD_FOLDER'], 'c.jpg'),
        "img4": os.path.join(app.config['UPLOAD_FOLDER'], 'd.jpg'),
    }

    # pred_image=None
    form = UploadForm()
    #form.submit.label.text = 'Predict'
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)

        print("this is file Name", filename)
        #predict_result = load_mode_and_predict("uploads/"+filename)
        predict_result = get_caption_prediction("uploads/" + filename)[0]
        pred_image = file_url
    else:
        predict_result = None
        pred_image = None
    return render_template('prediction.html', form=form, img_files=img_files, pred_image=pred_image, predict_result=predict_result)


if __name__ == '__main__':
    app.run()
