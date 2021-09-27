import joblib
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.neighbors import KNeighborsClassifier

def create_and_save_model():
    data = np.load(r'data.npz')
    trainX, trainy = data['arr_0'], data['arr_1']

    in_encoder = Normalizer(norm='l2')
    trainX = in_encoder.transform(trainX)
    
    out_encoder = LabelEncoder()
    out_encoder.fit(trainy)
    trainy = out_encoder.transform(trainy)
    print(trainy)

    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(trainX, trainy)

    if os.path.exists('models/knn_model.pkl'):
        print("model exists")
        return 
    joblib.dump(model, 'models/knn_model.pkl')

create_and_save_model()