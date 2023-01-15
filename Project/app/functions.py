import os
import cv2
import numpy as np
from skimage.transform import resize
from skimage.feature import hog
from skimage import exposure
from skimage import io, color, img_as_ubyte
from matplotlib import pyplot as plt
from skimage.feature import hog, greycomatrix, greycoprops, local_binary_pattern


def generateHistogramme_Color(filenames, progressBar):
    if not os.path.isdir("BGR"):
        os.mkdir("BGR")
    i=0
    for path in os.listdir(filenames):
        img = cv2.imread(filenames+"/"+path)
        histB = cv2.calcHist([img],[0],None,[256],[0,256])
        histG = cv2.calcHist([img],[1],None,[256],[0,256])
        histR = cv2.calcHist([img],[2],None,[256],[0,256])
        feature = np.concatenate((histB, np.concatenate((histG,histR),axis=None)),axis=None)

        num_image, _ = path.split(".")
        np.savetxt("BGR/"+str(num_image)+".txt" ,feature)
        progressBar.setValue(100*((i+1)/len(os.listdir(filenames))))
        i+=1
    print("indexation Hist Couleur terminée !!!!")

def generateHistogramme_HSV(filenames, progressBar):
    if not os.path.isdir("HSV"):
            os.mkdir("HSV")
    i=0
    for path in os.listdir(filenames):
        img = cv2.imread(filenames+"/"+path)
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = img[:,:,0], img[:,:,1], img[:,:,2]
        histH = cv2.calcHist([h],[0],None,[256],[0,256])
        histS = cv2.calcHist([s],[0],None,[256],[0,256])
        histV = cv2.calcHist([v],[0],None,[256],[0,256])

        feature = np.concatenate((histH, np.concatenate((histS,histV),axis=None)),axis=None)

        num_image, _ = path.split(".")
        np.savetxt("HSV/"+str(num_image)+".txt" ,feature)
        progressBar.setValue(100*((i+1)/len(os.listdir(filenames))))
        i+=1
        
    print("indexation HSV terminée !!!!")
    
        
def generateSIFT(filenames, progressBar):
    if not os.path.isdir("SIFT"):
        os.mkdir("SIFT")
    i=0
    for path in os.listdir(filenames):
        img = cv2.imread(filenames+"/"+path)
        featureSum = 0
        sift = cv2.SIFT_create()  
        kps , des = sift.detectAndCompute(img,None)

        num_image, _ = path.split(".")
        np.savetxt("SIFT/"+str(num_image)+".txt" ,des)
        progressBar.setValue(100*((i+1)/len(os.listdir(filenames))))
        
        featureSum += len(kps)
        i+=1
    print("Indexation SIFT terminée !!!!")    


def generateORB(filenames, progressBar):
    if not os.path.isdir("ORB"):
        os.mkdir("ORB")
    i=0
    for path in os.listdir(filenames):
        img = cv2.imread(filenames+"/"+path)
        orb = cv2.ORB_create()
        key_point1,descrip1 = orb.detectAndCompute(img,None)
        
        num_image, _ = path.split(".")
        np.savetxt("ORB/"+str(num_image)+".txt" ,descrip1 )
        progressBar.setValue(100*((i+1)/len(os.listdir(filenames))))
        i+=1
    print("indexation ORB terminée !!!!")
    
    
def generateGLCM(filenames, progressBar):
    if not os.path.isdir("GLCM"):
        os.mkdir("GLCM")
    distances=[1,-1]
    angles=[0, np.pi/4, np.pi/2, 3*np.pi/4]
    i=0
    for path in os.listdir(filenames):
        image = cv2.imread(filenames+"/"+path)
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        gray = img_as_ubyte(gray)
        glcmMatrix = greycomatrix(gray, distances=distances, angles=angles, normed=True)
        glcmProperties1 = greycoprops(glcmMatrix,'contrast').ravel()
        glcmProperties2 = greycoprops(glcmMatrix,'dissimilarity').ravel()
        glcmProperties3 = greycoprops(glcmMatrix,'homogeneity').ravel()
        glcmProperties4 = greycoprops(glcmMatrix,'energy').ravel()
        glcmProperties5 = greycoprops(glcmMatrix,'correlation').ravel()
        glcmProperties6 = greycoprops(glcmMatrix,'ASM').ravel()
        feature = np.array([glcmProperties1,glcmProperties2,glcmProperties3,glcmProperties4,glcmProperties5,glcmProperties6]).ravel()
        num_image, _ = path.split(".")
        np.savetxt("GLCM/"+str(num_image)+".txt" ,feature)
        progressBar.setValue(100*((i+1)/len(os.listdir(filenames))))
        i+=1
    print("indexation GLCM terminée !!!!")


def generateLBP(filenames, progressBar):
    if not os.path.isdir("LBP"):
        os.mkdir("LBP")
    i=0
    for path in os.listdir(filenames):
        img = cv2.imread(filenames+"/"+path)
        points=8
        radius=1
        method='default'
        subSize=(70,70)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img,(350,350))
        fullLBPmatrix = local_binary_pattern(img,points,radius,method)
        histograms = []
        for k in range(int(fullLBPmatrix.shape[0]/subSize[0])):
            for j in range(int(fullLBPmatrix.shape[1]/subSize[1])):
                subVector = fullLBPmatrix[k*subSize[0]:(k+1)*subSize[0],j*subSize[1]:(j+1)*subSize[1]].ravel()
                subHist,edges = np.histogram(subVector,bins=int(2**points),range=(0,2**points))
                histograms = np.concatenate((histograms,subHist),axis=None)
        num_image, _ = path.split(".")
        np.savetxt("LBP/"+str(num_image)+".txt" ,histograms)
        progressBar.setValue(100*((i+1)/len(os.listdir(filenames))))
        i+=1
    print("indexation LBP terminé !!!!")
    
    
def generateHOG(filenames, progressBar):
    if not os.path.isdir("HOG"):
        os.mkdir("HOG")
    i=0
    cellSize = (25,25)
    blockSize = (50,50)
    blockStride = (25,25)
    nBins = 9
    winSize = (350,350)
    for path in os.listdir(filenames):
        img = cv2.imread(filenames+"/"+path)
        image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image,winSize)
        hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nBins)
        feature = hog.compute(image)
        num_image, _ = path.split(".")
        np.savetxt("HOG/"+str(num_image)+".txt" ,feature )
        progressBar.setValue(100*((i+1)/len(os.listdir(filenames))))
        i+=1
    print("indexation HOG terminée !!!!")


def extractReqFeatures(fileName,descripteur_name):  
    # print(descripteur_name)
    if fileName: 
        img = cv2.imread(fileName)
        resized_img = resize(img, (128*4, 64*4))
            
        if descripteur_name=="BGR": #Couleurs
            histB = cv2.calcHist([img],[0],None,[256],[0,256])
            histG = cv2.calcHist([img],[1],None,[256],[0,256])
            histR = cv2.calcHist([img],[2],None,[256],[0,256])
            vect_features = np.concatenate((histB, np.concatenate((histG,histR),axis=None)),axis=None)
        
        elif descripteur_name=="HSV": # Histo HSV
            hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            histH = cv2.calcHist([hsv],[0],None,[256],[0,256])
            histS = cv2.calcHist([hsv],[1],None,[256],[0,256])
            histV = cv2.calcHist([hsv],[2],None,[256],[0,256])
            vect_features = np.concatenate((histH, np.concatenate((histS,histV),axis=None)),axis=None)

        elif descripteur_name=="SIFT": #SIFT
            sift = cv2.SIFT_create() #cv2.xfeatures2d.SIFT_create() pour py < 3.4 
            # Find the key point
            kps , vect_features = sift.detectAndCompute(img,None)
    
        elif descripteur_name=="ORB": #ORB
            orb = cv2.ORB_create()
            # finding key points and descriptors of both images using detectAndCompute() function
            key_point1,vect_features = orb.detectAndCompute(img,None)
                        
        elif descripteur_name=="GLCM": #GLCM
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            gray = img_as_ubyte(gray)
            glcm = greycomatrix(gray, distances=[1,-1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], normed=True)
            glcmProperties1 = greycoprops(glcm,'contrast').ravel()
            glcmProperties2 = greycoprops(glcm,'dissimilarity').ravel()
            glcmProperties3 = greycoprops(glcm,'homogeneity').ravel()
            glcmProperties4 = greycoprops(glcm,'energy').ravel()
            glcmProperties5 = greycoprops(glcm,'correlation').ravel()
            glcmProperties6 = greycoprops(glcm,'ASM').ravel()
            vect_features = np.array([glcmProperties1,glcmProperties2,glcmProperties3,glcmProperties4,glcmProperties5,glcmProperties6]).ravel()
            
        elif descripteur_name=="LBP": #LBP
            points=8
            radius=1
            method='default'
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img,(350,350))
            fullLBPmatrix = local_binary_pattern(img,points,radius,method)
            lbp_features = fullLBPmatrix.tolist()
            vect_features = np.array(lbp_features)
            
        elif descripteur_name=="HOG": #HOG
            cellSize = (25,25)
            blockSize = (50,50)
            blockStride = (25,25)
            nBins = 9
            winSize = (350,350)
            hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nBins)
            vect_features = hog.compute(img)

			
        np.savetxt("Methode_"+descripteur_name+"_requete.txt" ,vect_features)
        print("saved")
        #print("vect_features", vect_features)
        return vect_features