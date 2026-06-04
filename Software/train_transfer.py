import os
import tensorflow as tf

train_dir = "data/existing/SkinDisease/train"
test_dir = "data/existing/SkinDisease/test"

img_size = (224, 224)
batch_size = 32

train_data = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=img_size,
    batch_size=batch_size,
    label_mode="categorical"
)

test_data = tf.keras.utils.image_dataset_from_directory(
    test_dir,
    image_size=img_size,
    batch_size=batch_size,
    label_mode="categorical"
)

class_names = train_data.class_names
num_classes = len(class_names)

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

model = tf.keras.Sequential([
    tf.keras.layers.Rescaling(1./127.5, offset=-1),
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(num_classes, activation="softmax")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(
    train_data,
    validation_data=test_data,
    epochs=5
)

os.makedirs("models", exist_ok=True)
model.save("models/eosas_transfer_model.keras")

with open("models/class_names.txt", "w") as f:
    for name in class_names:
        f.write(name + "\n")

print("Transfer model saved to models/eosas_transfer_model.keras")
print("Class names saved to models/class_names.txt")