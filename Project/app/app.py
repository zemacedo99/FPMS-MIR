from flask import Flask, request, make_response, render_template
# import keras
import numpy as np
# from keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
# from keras.preprocessing.image import load_img, img_to_array
import os
from PIL import Image
from functions import extractReqFeatures, generateSIFT, generateHistogramme_HSV, generateHistogramme_Color, generateORB
from distances import *

app = Flask(__name__, static_folder='static')

#set paths to upload folder
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGE_UPLOADS'] = os.path.join(APP_ROOT, 'static')

filenames= "MIR_DATASETS_B"
filename = ""
top = 20

descripteurs_names = []
distances_names = []
features = []

@app.route("/mir",methods=["GET","POST"])
def mir():
    if request.method == "POST":
        global filename
        
        #read and upload resized files to folder
        image = request.files['input_file']
        filename = image.filename
        file_path = os.path.join(app.config["IMAGE_UPLOADS"], filename)
        image_pil = Image.open(image)
        image_pil.thumbnail((600,300), Image.ANTIALIAS)
        image_pil.save(file_path)
    
        checked_boxes = request.form.getlist('checkBox_name')
        
        for checked_box in checked_boxes:
            distance_name = checked_box.replace("checkBox", "dropdown")
            descripteur_name = checked_box.replace("checkBox_", "")
            distance = request.form[distance_name]
            distances_names.append(distance)
            descripteurs_names.append(descripteur_name)
            
        # print(distances_names)
        # print(descripteurs_names)
        
        global top
        top = request.form.get("number")
        # print("top", top)
        
        loadFeatures()
        #classify image
        # image = load_img(image, target_size=(224, 224))
        # image = img_to_array(image)
        # image = np.expand_dims(image, axis=0)
        # image = preprocess_input(image)
        # prediction = resnet_model.predict(image)
        # prediction = decode_predictions(prediction)[0][0][1]
        # prediction = prediction.replace('_',' ')
        
        #display prediction and image
        return render_template("upload.html", image_path = filename)
    return render_template("upload.html", image_path="landing_page_pic.jpg")

def loadFeatures():            

    for descripteur_name in descripteurs_names:
        model_path = os.path.join(os.path.dirname(APP_ROOT), descripteur_name)
        
        for j in os.listdir(model_path):
            data=os.path.join(model_path,j)
            # print(data)
            if not data.endswith(".txt"):
                continue
            feature = np.loadtxt(data)
            features.append((os.path.join(filenames,os.path.basename(data).split('.')[0]+'.jpg'),feature))
            
    Recherche()
 
            
            
def Recherche():
    global filename
    voisins=""
    
    if descripteurs_names != []:
        
        for i,descripteur_name in enumerate(descripteurs_names):  
            print(descripteur_name)
            print(i)
            ##Generer les features de l'images requete
            filename_path = os.path.join(APP_ROOT, 'static')
            fileName = os.path.join(filename_path, filename)
            req = extractReqFeatures(fileName, descripteur_name)

            #Aller chercher dans la liste de l'interface la distance choisie
            distanceName=distances_names[i]
            # print(distanceName)
            # print(top)
        
            #Générer les voisins
            voisins=getkVoisins(features, req, top, distanceName )

        # self.path_image_plus_proches = []
        # self.nom_image_plus_proches = []
        # for k in range(top):
        #     self.path_image_plus_proches.append(voisins[k][0])
        #     self.nom_image_plus_proches.append(os.path.basename(voisins[k][0]))
            
        # #Nombre de colonnes pour l'affichage
        # if top <= 10:
        #     col=3
        # elif top <= 20:
        #     col = 5
        # else:
        #     col = 10
            
        # k=0
        # for i in range(math.ceil(top/col)):
        #     for j in range(col):
        #         if os.path.exists(self.path_image_plus_proches[k]):
        #             img = cv2.imread(self.path_image_plus_proches[k],1) #load image
        #         else:
        #             print("Image not found: ", self.path_image_plus_proches[k])
                    
        #         #Remise de l'image en RGB pour l'afficher correctement
        #         b,g,r = cv2.split(img) # get b,g,r
        #         img = cv2.merge([r,g,b]) # switch it to rgb
        #         #convert image to QImage
        #         height, width, channel = img.shape
        #         bytesPerLine = 3 * width
        #         qImg = QtGui.QImage(img.data, width, height, bytesPerLine,
        #         QtGui.QImage.Format_RGB888)

        #         pixmap=QtGui.QPixmap.fromImage(qImg)
        #         label = QtWidgets.QLabel("")
        #         label.setAlignment(QtCore.Qt.AlignCenter)
        #         label.setPixmap(pixmap.scaled(0.3*width, 0.3*height,
        #         QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        #         self.gridLayout.addWidget(label, i, j)
        #         k+=1
    else :
        print("Il faut choisir une méthode !")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)