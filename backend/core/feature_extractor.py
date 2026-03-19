import cv2
import numpy as np
from skimage.feature import local_binary_pattern, hog
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import easyocr
import os

# CNN Globals
cnn_model = None

def get_cnn_model():
    global cnn_model
    if cnn_model is None:
        cnn_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    return cnn_model

def extract_cnn_features(image):
    model = get_cnn_model()
    img_resized = cv2.resize(image, (224, 224))
    img_array = img_to_array(img_resized)
    img_expanded = np.expand_dims(img_array, axis=0)
    img_preprocessed = preprocess_input(img_expanded)
    features = model.predict(img_preprocessed, verbose=0)
    return features.flatten()

def extract_sift_features(gray_image):
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(gray_image, None)
    return len(keypoints), descriptors

def extract_orb_features(gray_image):
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(gray_image, None)
    return len(keypoints), descriptors

def extract_hog_features(gray_image):
    img_resized = cv2.resize(gray_image, (128, 256))
    features = hog(img_resized, orientations=9, pixels_per_cell=(8, 8),
                   cells_per_block=(2, 2), visualize=False)
    return features

def extract_lbp_features(gray_image):
    radius = 3
    n_points = 8 * radius
    lbp = local_binary_pattern(gray_image, n_points, radius, method='uniform')
    (hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0, n_points + 3), range=(0, n_points + 2))
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)
    return hist

# OCR Globals
reader = None

def get_ocr_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['en'], gpu=False)
    return reader

def extract_document_text(image):
    try:
        ocr_reader = get_ocr_reader()
        results = ocr_reader.readtext(image)
        text = " ".join([res[1] for res in results])
        return text if text.strip() else "No text detected."
    except Exception as e:
        return f"OCR processing failed: {str(e)}"

# Primary Export function
def get_extracted_features(processed_image_dict, techniques=None):
    if techniques is None:
        techniques = ['CNN', 'SIFT', 'HOG', 'LBP', 'ORB']

    original = processed_image_dict['original']
    gray = processed_image_dict['gray']
    
    results = {}
    summary_parts = []

    if 'CNN' in techniques:
        cnn_feats = extract_cnn_features(original)
        results['cnn_vector_size'] = len(cnn_feats)
        summary_parts.append(f"{len(cnn_feats)} CNN deep features")
    
    if 'HOG' in techniques:
        hog_feats = extract_hog_features(gray)
        results['hog_vector_size'] = len(hog_feats)
        summary_parts.append(f"{len(hog_feats)} HOG shape parameters")
    
    if 'LBP' in techniques:
        lbp_feats = extract_lbp_features(gray)
        results['lbp_vector_size'] = len(lbp_feats)
        summary_parts.append("LBP texture anomalies")
    
    if 'SIFT' in techniques:
        sift_kp_count, _ = extract_sift_features(gray)
        results['sift_keypoints'] = sift_kp_count
        summary_parts.append(f"{sift_kp_count} SIFT keypoints")
    
    if 'ORB' in techniques:
        orb_kp_count, _ = extract_orb_features(gray)
        results['orb_keypoints'] = orb_kp_count
        summary_parts.append(f"{orb_kp_count} ORB keypoints")
    
    results['extracted_text'] = extract_document_text(original)
    results['extracted_features_summary'] = "Extracted: " + ", ".join(summary_parts) + "."
    results['simulated_anomaly_score'] = float(np.random.uniform(0.78, 0.99))
    
    return results
