from keras.models import load_model
network = None;
import os
import PIL
import numpy as np
from PIL import Image
imageHeight = 240
imageWith = 240
numberOfCanal = 1
typeOfImageResizeAproxymation = PIL.Image.ANTIALIAS


def LoadModel(pathToModel):
    network = load_model(pathToModel)
    return network


def Loaddata(image):
    oneImg = Image.open(image)
    oneImg = oneImg.resize((imageWith, imageHeight), typeOfImageResizeAproxymation)
    tablizedImage = np.array(oneImg.getdata()).reshape(1, imageWith, imageHeight, numberOfCanal)
    tablizedImage = tablizedImage/255
    return tablizedImage


def Predict(network, image):
    dataset = Loaddata(image)

    result = network.predict_classes(dataset)

    if(result[0]==1):
        return True
    else:
        return False


def main(image):
    dirname = os.path.dirname(__file__)
    path_to_network = os.path.join(dirname, 'network')
    print("Main function of the module")
    network = LoadModel(path_to_network)

    result = Predict(network, image)
    return result