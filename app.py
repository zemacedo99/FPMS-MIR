from flask import Flask, request, make_response, render_template
import keras
import numpy as np
from keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from keras.preprocessing.image import load_img, img_to_array
import os
from PIL import Image

app = Flask(__name__)

#set paths to upload folder
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGE_UPLOADS'] = os.path.join(APP_ROOT, 'static')

@app.route("/image-classifier",methods=["GET","POST"])
def classify_image():
    if request.method == "POST":
        
        #read and upload resized files to folder
        image = request.files['input_file']
        filename = image.filename
        file_path = os.path.join(app.config["IMAGE_UPLOADS"], filename)
        image_pil = Image.open(image)
        image_pil.thumbnail((600,300), Image.ANTIALIAS)
        image_pil.save(file_path)
        
        #classify image
        image = load_img(image, target_size=(224, 224))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)
        prediction = resnet_model.predict(image)
        prediction = decode_predictions(prediction)[0][0][1]
        prediction = prediction.replace('_',' ')
        
        #display prediction and image
        return render_template("upload.html", image_path = filename, prediction = 'Prediction: '+prediction)
    return render_template("upload.html", image_path = 'landing_page_pic.jpg')

if __name__ == '__main__':
    resnet_model = ResNet50(weights='imagenet')
    app.run(host='0.0.0.0', debug=False, threaded=False, port=8000)