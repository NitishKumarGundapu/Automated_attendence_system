import os
import cv2
import dlib
import PIL.Image
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.neighbors import KNeighborsClassifier

face_detector = dlib.get_frontal_face_detector()

predictor_68_point_model = "models\\shape_predictor_68_face_landmarks.dat"
pose_predictor_68_point = dlib.shape_predictor(predictor_68_point_model)

face_recognition_model = "models\\dlib_face_recognition_resnet_model_v1.dat"
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)

def load_image_file(file, mode='RGB'):
    im = PIL.Image.open(file)
    if mode:
        im = im.convert(mode)
    return np.array(im)

def _raw_face_locations(img, number_of_times_to_upsample=1):
    return face_detector(img, number_of_times_to_upsample)

def _raw_face_landmarks(face_image, face_locations=None, model="large"):
    face_locations = _raw_face_locations(face_image)
    pose_predictor = pose_predictor_68_point
    return [pose_predictor(face_image, face_location) for face_location in face_locations]

def face_encodings(face_image, known_face_locations=None, num_jitters=1, model="large"):
    raw_landmarks = _raw_face_landmarks(face_image, known_face_locations, model)
    return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set,num_jitters)) for raw_landmark_set in raw_landmarks]

def create_face(z):
    FACE_DIR = "data/train/"
    if not os.path.exists(FACE_DIR):
        os.mkdir(FACE_DIR)
    while True:
        name = z
        try:
            face_folder = FACE_DIR + name + "/"
            if not os.path.exists(face_folder):
                os.mkdir(face_folder)
            break
        except:
            print("Invalid input.!")
            continue

    init_img_no = int(len(os.listdir(face_folder)))
    img_no = init_img_no
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    total_imgs = 50
    while True:
        ret, img = cap.read()
        img_path = face_folder +name+ str(img_no) + ".jpg"
        cv2.imwrite(img_path, img)
        cv2.imshow("aligned", img)
        img_no += 1

        cv2.imshow("Saving", img)
        cv2.waitKey(100)
        if img_no == init_img_no + total_imgs:
            break
    cap.release()
    cv2.destroyAllWindows()

def extract_faces(filename):
    image = load_image_file(filename)
    face_encoding = face_encodings(image)
    return face_encoding

def get_faces(image_path):

    data = np.load(r'data.npz')
    trainX, trainy = data['arr_0'], data['arr_1']

    in_encoder = Normalizer(norm='l2')
    trainX = in_encoder.transform(trainX)
    
    out_encoder = LabelEncoder()
    out_encoder.fit(trainy)
    trainy = out_encoder.transform(trainy)

    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(trainX, trainy)

    presenties = []

    faces = extract_faces(image_path)

    for a in faces:
        test_image = np.array([a])
        test_image = in_encoder.transform(test_image)

        yhat_class = model.predict(test_image)
        class_index = round(yhat_class[0])
        yhat_class[0] = class_index
        predict_names = out_encoder.inverse_transform([class_index])
        presenties.append((predict_names[0]))

    return presenties
