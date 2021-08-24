from os import listdir
from os.path import isdir
import numpy as np
import Mlpart

def extract_face(filename):
    image = Mlpart.load_image_file(filename)
    face_encoding = Mlpart.face_encodings(image)
    try :
        return np.array(face_encoding[0])
    except :
        print(filename)

def load_faces(directory):
	faces = list()
	for filename in listdir(directory):
		path = directory + filename
		face = extract_face(path)
		faces.append(face)
	return faces

def load_dataset(directory):
	X, y = list(), list()
	for subdir in listdir(directory):
		path = directory + subdir + '/'
		if not isdir(path):
			continue
		faces = load_faces(path)
		labels = [subdir for _ in range(len(faces))]
		print('=> loaded %d FACES for class: %s' % (len(faces), subdir))
		X.extend(faces)
		y.extend(labels)
	return np.asarray(X), np.asarray(y)

trainX, trainy = load_dataset("data\\train\\")
print('Loaded: ', trainX.shape, trainy.shape)
np.savez_compressed('data.npz', trainX, trainy)
print("dataset is created")