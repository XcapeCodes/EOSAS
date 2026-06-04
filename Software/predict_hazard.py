import sys
import cv2
import numpy as np
import tensorflow as tf

MODEL_PATH = "models/eosas_transfer_v2.keras"
CLASS_NAMES_PATH = "models/class_names.txt"

hazard_weights = {
    "Unknown_Normal": 0,
    "Acne": 35,
    "Eczema": 45,
    "Rosacea": 45,
    "Tinea": 50,
    "Candidiasis": 50,
    "Infestations_Bites": 55,
    "Sun_Sunlight_Damage": 55,
    "Moles": 45,
    "Warts": 50,
    "Vitiligo": 40,
    "Psoriasis": 60,
    "Lichen": 60,
    "Seborrh_Keratoses": 55,
    "Actinic_Keratosis": 70,
    "DrugEruption": 70,
    "Bullous": 75,
    "Benign_tumors": 65,
    "Vascular_Tumors": 75,
    "Vasculitis": 80,
    "Lupus": 80,
    "SkinCancer": 95
}

def load_class_names(path):
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]

def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    img = cv2.resize(img, (224, 224))
    img = img.astype("float32")
    img = np.expand_dims(img, axis=0)
    return img

def main():
    if len(sys.argv) < 2:
        print("Usage: python predict_hazard.py path_to_image.jpg")
        return

    image_path = sys.argv[1]

    model = tf.keras.models.load_model(MODEL_PATH)
    class_names = load_class_names(CLASS_NAMES_PATH)

    img = preprocess_image(image_path)
    predictions = model.predict(img)[0]

    top_index = int(np.argmax(predictions))
    top_class = class_names[top_index]
    confidence = float(predictions[top_index])

    # Weighted hazard score using all probabilities
    hazard_score = 0

    for i, prob in enumerate(predictions):
        class_name = class_names[i]
        weight = hazard_weights.get(class_name, 50)
        hazard_score += prob * weight

    hazard_score = int(hazard_score)

    top_3_indices = predictions.argsort()[-3:][::-1]

    print("\nEOSAS Skin Analysis Result")
    print("--------------------------")
    print(f"Image: {image_path}")
    print(f"Hazard Score: {hazard_score}/100")
    print(f"Main visual pattern: {top_class}")
    print(f"Confidence: {confidence * 100:.2f}%")

    print("\nTop visual matches:")
    for i in top_3_indices:
        class_name = class_names[i]
        prob = predictions[i] * 100
        print(f"- {class_name}: {prob:.2f}%")

    print("\nNote: This is not a medical diagnosis. It is an experimental visual hazard score.")

if __name__ == "__main__":
    main()