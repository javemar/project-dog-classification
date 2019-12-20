import  tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.applications.resnet50 import preprocess_input#, decode_predictions
import numpy as np
from PIL import ImageFile
import cv2
import pickle

MODEL_TRANSFER  = tf.keras.models.load_model("models/breed_model_v5_79.78.h5")
FACE_CASCADE = cv2.CascadeClassifier('models/haarcascade_frontalface_alt.xml')
with open("models/classes.pk", "rb") as fl:
	INVERSE_DICT_CLASS = pickle.load(fl)
#img = cv2.imread(human_files[0])
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ImageFile.LOAD_TRUNCATED_IMAGES = True


SIZE_SHAPE = 224
IMG_SHAPE = (SIZE_SHAPE,SIZE_SHAPE,3)


tf_model = tf.keras.applications.ResNet50(input_shape=IMG_SHAPE, include_top=True, weights='imagenet' )

def face_detector(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(gray)
    return len(faces) > 0


def dog_detector_versiontf(img_path,IMG_SHAPE=IMG_SHAPE  ):
    test_img = tf.keras.preprocessing.image.load_img(img_path,target_size=IMG_SHAPE)
    test_img = tf.keras.preprocessing.image.img_to_array(test_img)
    test_img = tf.keras.applications.resnet50.preprocess_input(test_img)
    #test_img  = cv2.resize(plt.imread(dog_files[j],cv2.IMREAD_COLOR),(SIZE_SHAPE,SIZE_SHAPE))/SIZE_SHAPE

    prediccion = tf_model.predict(test_img.reshape(-1,SIZE_SHAPE,SIZE_SHAPE,3))
    index_prediccion = prediccion.argmax()
    #print (index_prediccion)
    return index_prediccion<=268 and index_prediccion>=151 
	
def predict_breed_transfer(img_path):
    
    img = tf.keras.preprocessing.image.load_img(img_path,target_size=IMG_SHAPE)
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = tf.keras.applications.resnet50.preprocess_input(img)
    img = np.expand_dims(img,axis=0)
    
    prediction = MODEL_TRANSFER.predict(img).argmax()
#     print (prediction.shape)
    prediction_class = INVERSE_DICT_CLASS[prediction]
    # load the image and return the predicted breed
    return prediction_class

def run_app_get_labels(img_path):
    img = cv2.imread(img_path)
    ## handle cases for a human face, dog, and neither
    human = face_detector(img_path)
    dog = dog_detector_versiontf(img_path)
    
    if dog or human:
        if dog:
            title = "Hello dog :D"
            
            
        elif human:
            title = "Hello human :D"
#         print(plt.imshow(img));
        name_dog = predict_breed_transfer(img_path)
        xlabel = "You look like {}".format(name_dog)
    else: 
        #print(plt.imshow(img));
        title = "You  don't look like a human or dog"
        xlabel = ""
    #plt.imshow(img)
    #plt.title(title)
    #plt.xlabel(xlabel.replace("_",  "" ))
    #plt.show()
    return title, xlabel