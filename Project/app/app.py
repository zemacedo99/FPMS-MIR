from flask import Flask, request, make_response, render_template
# import keras
import numpy as np
# from keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
# from keras.preprocessing.image import load_img, img_to_array
import os
from PIL import Image
import base64
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
path_image_plus_proches = []
nom_image_plus_proches = []
imgs = []
RPgraph = ""

@app.route("/")
def homepage():
    return render_template("upload.html")

@app.route("/homepage",methods=["GET"])
def homepage1():
    return render_template("upload.html")


@app.route("/load",methods=["GET","POST"])
def loadfunction():
    if request.method == "POST":
        global filename
        global descripteurs_names
        global distances_names
        
        #read and upload resized files to folder
        image = request.files['input_file']
        filename = image.filename
        file_path = os.path.join(app.config["IMAGE_UPLOADS"], filename)
        image_pil = Image.open(image)
        image_pil.thumbnail((600,300), Image.ANTIALIAS)
        image_pil.save(file_path)
    
        checked_boxes = request.form.getlist('checkBox_name')
        
        distances_names = []
        descripteurs_names = []
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
        Recherche()
        rappel_precision()
        return render_template('result.html', image_path = filename, imgs=imgs, top=top, RPgraph=RPgraph)

def loadFeatures():            

    global features
    features = []
    
    for descripteur_name in descripteurs_names:
        model_path = os.path.join(os.path.dirname(APP_ROOT), descripteur_name)
        
        for j in os.listdir(model_path):
            data=os.path.join(model_path,j)
            # print(data)
            if not data.endswith(".txt"):
                continue
            feature = np.loadtxt(data)
            features.append((os.path.join(filenames,os.path.basename(data).split('.')[0]+'.jpg'),feature))

 
            
def Recherche():
    global filename
    global distanceName
    global imgs
    global path_image_plus_proches
    global nom_image_plus_proches
    
    voisins=""
    
    if descripteurs_names != []:
        
        for i,descripteur_name in enumerate(descripteurs_names):  
            # print(descripteur_name)
            # print(i)
            ##Generer les features de l'images requete
            filename_path = os.path.join(APP_ROOT, 'static')
            fileName = os.path.join(filename_path, filename)
            req = extractReqFeatures(fileName, descripteur_name)

            #Aller chercher dans la liste de l'interface la distance choisie
            distanceName=distances_names[i]
            # print(distanceName)
            # print(top)
        
            #G??n??rer les voisins
            voisins=getkVoisins(features, req, top, distanceName )
            
        imgs = []
        path_image_plus_proches = []
        nom_image_plus_proches =[]
        
        for k in range(int(top)):
            path_image_plus_proches.append(voisins[k][0])
            nom_image_plus_proches.append(os.path.basename(voisins[k][0]))
            
            image_path = os.path.join(os.path.dirname(APP_ROOT), path_image_plus_proches[k])
            # print("image_path")
            # print(image_path)

            if os.path.exists(image_path):
                img = cv2.imread(image_path,1) #load image
                ret, buffer = cv2.imencode('.jpg', img)
                img_base64 = base64.b64encode(buffer).decode()
                imgs.append(img_base64)
            else:
                print("Image not found: ", path_image_plus_proches[k])
            
    else :
        print("Il faut choisir une m??thode !")


def rappel_precision():
        rappel_precision=[]
        rappels=[]
        precisions=[]
        average_precisions = []
        global RPgraph

        filename_path = os.path.join(APP_ROOT, 'static')
        fileName = os.path.join(filename_path, filename)
        filename_parts = fileName.split("_")

        num_image = filename_parts[-1].split(".")[0]
        
        image_folder = filename_parts[2]
        
        classe_image_requete = image_folder
        val =0

        for j in range(int(top)):
            filename_parts = nom_image_plus_proches[j].split('_')
            # print(filename_parts)
            image_folder = filename_parts[2]
            classe_image_proche = image_folder
            # print("classe_image_proche", classe_image_proche)
            # print("classe_image_requete", classe_image_requete)
            if classe_image_requete==classe_image_proche:
                rappel_precision.append(True) #Bonne classe (pertinant)
                val += 1
            else:
                rappel_precision.append(False) #Mauvaise classe (non pertinant)
                
        for i in range(int(top)):
            j=i
            val=0
            while(j>=0):
                if rappel_precision[j]:
                    val+=1
                j-=1
            precision = val/(i+1)
            rappel = val/int(top)
            rappels.append(rappel)
            precisions.append(precision)
            
        precisions = np.asarray(precisions)
        rappels = np.asarray(rappels)
        average_precision = np.trapz(precisions, x=rappels)  

        #Cr??ation de la courbe R/P
        plt.plot(rappels,precisions)
        # plt.plot(rappels, average_precisions, 'g--', label='average precision')
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.title("R/P"+str(top)+" voisins de l'image n??"+num_image)


        val = np.cumsum(rappel_precision)
        precision = val / np.arange(1, int(top)+1)
        rappel = val / int(top)

        # Print the precision and recall
        print("Precision:", precision)
        print("Recall:", rappel)
        print("average_precision", average_precision)

        
        #Enregistrement de la courbe RP
        save_folder=os.path.join(".",num_image)
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        save_name=os.path.join(save_folder,num_image+'.png')
        plt.savefig(save_name,format='png',dpi=600)
        plt.close()

        #Affichage de la courbe R/P
        img = cv2.imread(save_name,1) #load image in color
        ret, buffer = cv2.imencode('.jpg', img)
        RPgraph = base64.b64encode(buffer).decode()
        
        
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)