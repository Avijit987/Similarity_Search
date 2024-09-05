import os
import numpy as np
from PIL import Image
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity

# Load pre-trained VGG16 model for feature extraction
model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

def extract_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = model.predict(img_data)
    return features.flatten()

def find_similar_images(query_image_path, image_folder):
    query_features = extract_features(query_image_path)
    similarities = []
    for img_name in os.listdir(image_folder):
        img_path = os.path.join(image_folder, img_name)
        img_features = extract_features(img_path)
        similarity = cosine_similarity([query_features], [img_features])
        similarities.append((img_name, similarity[0][0]))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:5]  # Return top 5 similar images
