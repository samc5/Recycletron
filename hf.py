# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("image-classification", model="hmrizal/recycled_waste_classification")

# Load model directly
from transformers import AutoImageProcessor, AutoModelForImageClassification

processor = AutoImageProcessor.from_pretrained("hmrizal/recycled_waste_classification")
model = AutoModelForImageClassification.from_pretrained("hmrizal/recycled_waste_classification")