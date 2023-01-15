from flask import Flask, request, make_response, render_template
# import keras
import numpy as np
# from keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
# from keras.preprocessing.image import load_img, img_to_array
import os
from PIL import Image

app = Flask(__name__, static_folder='static')

#set paths to upload folder
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGE_UPLOADS'] = os.path.join(APP_ROOT, 'static')

filenames= "MIR_DATASETS_B"

@app.route("/mir",methods=["GET","POST"])
def mir():
    if request.method == "POST":
        
        #read and upload resized files to folder
        image = request.files['input_file']
        filename = image.filename
        file_path = os.path.join(app.config["IMAGE_UPLOADS"], filename)
        image_pil = Image.open(image)
        image_pil.thumbnail((600,300), Image.ANTIALIAS)
        image_pil.save(file_path)
        
    
        checked_boxes = request.form.getlist('checkBox_name')
        print("checked_boxes")
        print(checked_boxes)
        
        number = request.form.get("number")
        print("top", number)
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
        folder_model=""
        
        if checkBox_HistC.isChecked():
            folder_model = './BGR'
            algo_choice=1
            
        if checkBox_HSV.isChecked():
            folder_model = './HSV'
            algo_choice=2
            
        if checkBox_SIFT.isChecked():
            folder_model = './SIFT'
            algo_choice=3
            
        if checkBox_ORB.isChecked():
            folder_model = './ORB'
            algo_choice=4
                        
        if checkBox_GLCM.isChecked():
            folder_model = './GLCM'
            algo_choice=5
                                
        if checkBox_LBP.isChecked():
            folder_model = './LBP'
            algo_choice=6
                                    
        if checkBox_HOG.isChecked():
            folder_model = './HOG'
            algo_choice=7
            
            
        # if filenames:
        #     if algo_choice==3 or algo_choice==4:
        #         comboBox.clear()
        #         comboBox.addItems(["Brute force","Flann"])
        #     else :
        #         comboBox.clear()
        #         comboBox.addItems(["Euclidienne","Correlation","Chicarre","Intersection","Bhattacharyya"])
                
        if len(filenames)<1:
            print("Merci de charger une image avec le bouton Ouvrir")
            
        ##Charger les features de la base de données.
        self.features1 = []
        pas=0
        print("chargement de descripteurs en cours ...")
        
        for j in os.listdir(folder_model): #folder_model : dossier de features
            data=os.path.join(folder_model,j)
            if not data.endswith(".txt"):
                continue
            feature = np.loadtxt(data)
            self.features1.append((os.path.join(filenames,os.path.basename(data).split('.')[0]+'.jpg'),feature))
            pas += 1
            self.progressBar.setValue(int(100*((pas+1)/1000)))
            
        if not self.checkBox_SIFT.isChecked() and not self.checkBox_HistC.isChecked() and not self.checkBox_HSV.isChecked() and not self.checkBox_ORB.isChecked() and not self.checkBox_GLCM.isChecked() and not self.checkBox_LBP.isChecked() and not self.checkBox_HOG.isChecked():
            print("Merci de sélectionner au moins un descripteur dans le menu")
            showDialog()
        print("chargement des descripteurs terminé")
            
            
def Recherche(self, MainWindow):
    #Remise à 0 de la grille des voisins
    for i in reversed(range(self.gridLayout.count())):
        self.gridLayout.itemAt(i).widget().setParent(None)
    voisins=""
    if self.algo_choice !=0:
        ##Generer les features de l'images requete
        req = extractReqFeatures(fileName, self.algo_choice)
        ##Definition du nombre de voisins
        self.sortie = 20
        #Aller chercher dans la liste de l'interface la distance choisie
        distanceName=self.comboBox.currentText()
        #Générer les voisins
        voisins=getkVoisins(self.features1, req, self.sortie, distanceName )

        self.path_image_plus_proches = []
        self.nom_image_plus_proches = []
        for k in range(self.sortie):
            self.path_image_plus_proches.append(voisins[k][0])
            self.nom_image_plus_proches.append(os.path.basename(voisins[k][0]))
        #Nombre de colonnes pour l'affichage
        if self.sortie <= 10:
            col=3
        elif self.sortie <= 20:
            col = 5
        else:
            col = 10
            
        k=0
        for i in range(math.ceil(self.sortie/col)):
            for j in range(col):
                if os.path.exists(self.path_image_plus_proches[k]):
                    img = cv2.imread(self.path_image_plus_proches[k],1) #load image
                else:
                    print("Image not found: ", self.path_image_plus_proches[k])
                    
                #Remise de l'image en RGB pour l'afficher correctement
                b,g,r = cv2.split(img) # get b,g,r
                img = cv2.merge([r,g,b]) # switch it to rgb
                #convert image to QImage
                height, width, channel = img.shape
                bytesPerLine = 3 * width
                qImg = QtGui.QImage(img.data, width, height, bytesPerLine,
                QtGui.QImage.Format_RGB888)

                pixmap=QtGui.QPixmap.fromImage(qImg)
                label = QtWidgets.QLabel("")
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setPixmap(pixmap.scaled(0.3*width, 0.3*height,
                QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
                self.gridLayout.addWidget(label, i, j)
                k+=1
    else :
        print("Il faut choisir une méthode !")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)