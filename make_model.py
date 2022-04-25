from tflite_model_maker import image_classifier
from tflite_model_maker.image_classifier import DataLoader

data = DataLoader.from_folder('./birds/')

model = image_classifier.create(data)

loss, accuracy = model.evaluate()

model.export(export_dir='./export/')

