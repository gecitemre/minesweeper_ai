from tensorflow import keras

data = keras.preprocessing.image_dataset_from_directory(
    "data", label_mode="categorical"
)

model = keras.models.Sequential(
    (
        keras.layers.Resizing(32,32),
        keras.layers.Flatten(),
        keras.layers.Rescaling(1 / 255),
        keras.layers.Dense(len(data.class_names), activation="softmax"),
    )
)
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(data, epochs=20)
model.save_weights("weights")