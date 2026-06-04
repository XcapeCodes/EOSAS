import sys
import cv2
import numpy as np
import tensorflow as tf

MODEL_PATH = "models/eosas_hazard_model.keras"
CLASS_NAMES_PATH = "models/hazard_class_names.txt"

score_map = {
    "Low_Hazard": 15,
    "Medium_Hazard": 55,
    "High_Hazard": 90
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
        print("Usage: python predict_hazard_level.py image_path")
        return

    image_path = sys.argv[1]

    model = tf.keras.models.load_model(MODEL_PATH)
    class_names = load_class_names(CLASS_NAMES_PATH)

    img = preprocess_image(image_path)
    predictions = model.predict(img)[0]

    top_index = int(np.argmax(predictions))
    top_class = class_names[top_index]
    confidence = float(predictions[top_index])

    hazard_score = 0
    for i, prob in enumerate(predictions):
        class_name = class_names[i]
        hazard_score += prob * score_map.get(class_name, 50)

    hazard_score = int(hazard_score)

    top_indices = predictions.argsort()[-3:][::-1]

    print("\nEOSAS Hazard Result")
    print("-------------------")
    print(f"Image: {image_path}")
    print(f"Hazard Level: {top_class}")
    print(f"Hazard Score: {hazard_score}/100")
    print(f"Confidence: {confidence * 100:.2f}%")

    print("\nTop matches:")
    for i in top_indices:
        print(f"- {class_names[i]}: {predictions[i] * 100:.2f}%")

    print("\nNote: This is not a medical diagnosis.")

if __name__ == "__main__":
    main()