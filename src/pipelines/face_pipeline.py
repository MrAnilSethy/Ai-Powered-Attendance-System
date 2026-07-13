import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st 
from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()
    
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    
    facerecog = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector,sp,facerecog


#face embeddings
def get_face_embeddings(img_np):
    detector,sp,facerecog = load_dlib_models()
    faces = detector(img_np,1)
    
    encodings = []
    for face in faces:
        shape = sp(img_np,face)
        face_descriptor = facerecog.compute_face_descriptor(img_np,shape,1) #128 embedging
        encodings.append(np.array(face_descriptor))
    return encodings

#train model
@st.cache_resource
def get_trained_model():
    X = []
    y = []
    
    student_db = get_all_students()
    if not student_db:
        return None
    for student in student_db:
        embedding = student.get('face_embedding')
        X.append(np.array(embedding))
        y.append(student.get('student_id'))
    if len(X) == 0:
        return None
    clf = SVC(kernel='linear',probability=True,class_weight='balanced')
    try:
        clf.fit(X,y)
    except ValueError:
        pass
    return {'clf':clf,'X':X,'Y':y}

#for new face re-run model
def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

#attendance predict
def predict_attendance(class_img_np):
    encodings = get_face_embeddings(class_img_np)
    detected_student = {}
    
    model_data = get_trained_model()
    
    if not model_data:
        return detected_student,[],0 #student,prediction,count
    clf = model_data['clf']
    X_train = model_data['X'] #embeddings
    y_train = model_data['y'] #student_ids
    
    
    all_students = sorted(list(set(y_train))) #all student ids
    
    for encoding in encodings:
        if len(all_students)>=2:
            predicted_id = int(clf.predict([encoding])[0]) #0 for high-proba
        else:
            predicted_id = int(all_students[0])
            
        student_embedding = X_train[y_train.index(predicted_id)] #X_train index == y_train_index
        best_match_score = np.linalg.norm(student_embedding-encoding)
        
        resemblance_threshold = 0.6
        
        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True
    return detected_student,all_students,len(encoding)

    
    