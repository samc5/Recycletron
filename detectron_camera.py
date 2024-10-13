import cv2
import torch
import torchvision
import detectron2
from detectron2.utils.logger import setup_logger
from io import BytesIO

from PIL import Image
import io
import base64
setup_logger()

import numpy as np
import os, json, cv2, random

# import detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

# Helper function to perform predictions and visualize results
def predict_and_visualize(image, predictor, cfg):
    # Perform detection on the image
    outputs = predictor(image)

    # Visualize the predictions
    v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

    # Convert the output frame back to BGR format for OpenCV
    detected_frame = out.get_image()[:, :, ::-1]

    instances = outputs["instances"].to("cpu")  # Move instances to CPU for easier handling
    predicted_classes = instances.pred_classes.numpy()

    # Get metadata for COCO dataset
    metadata = MetadataCatalog.get("coco_2017_train")

    # Access class names
    class_names = metadata.thing_classes
    predicted_labels = [class_names[i] for i in predicted_classes]

    # Return the visualized image and predicted labels
    return detected_frame, predicted_labels

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

        # Setup the config for the model
        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # Set threshold for this model
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        self.cfg.MODEL.DEVICE = "cpu"
        
        # Set up the predictor
        self.predictor = DefaultPredictor(self.cfg)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        # Capture a frame from the video stream
        ret, frame = self.video.read()

        # Use the shared prediction function
        detected_frame, predicted_labels = predict_and_visualize(frame, self.predictor, self.cfg)

        # Encode the frame as JPEG
        ret, jpeg = cv2.imencode('.jpg', detected_frame)
        
        # Return the encoded frame and the predicted labels
        print(predicted_labels)  # For debugging purposes
        return jpeg.tobytes()

# Function to process a static image file
def get_classes(image_path, dest_path):
    # Read the image from the file path
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError(f"Failed to load image from path: {image_path}")

    # Create a configuration for the predictor (same as in VideoCamera)
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.MODEL.DEVICE = "cpu"

    # Initialize the predictor
    predictor = DefaultPredictor(cfg)

    # Use the shared prediction function
    detected_frame, predicted_labels = predict_and_visualize(image, predictor, cfg)

    # Encode the frame as JPEG

    success, jpeg = cv2.imencode('.jpg', detected_frame)

    if success:
        # Save the JPEG bytes to a file
        with open(dest_path, 'wb') as f:
            f.write(jpeg.tobytes())  # Convert the encoded image to bytes and write to the file
        print(f"Image saved successfully at {dest_path}")
    else:
        print("Failed to encode image.")
    
    # Return the encoded image and predicted labels
    return jpeg, predicted_labels


def resize_image(image, max_width, max_height):
    # Open the image using PIL
    img = Image.open(io.BytesIO(image))

    # Get original dimensions
    original_width, original_height = img.size

    # Calculate aspect ratio
    aspect_ratio = original_width / original_height

    # Compute new dimensions based on the aspect ratio
    if original_width > original_height:
        new_width = min(max_width, original_width)
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = min(max_height, original_height)
        new_width = int(new_height * aspect_ratio)

    # Resize image
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    buffered = BytesIO()
    img.save(buffered, format="JPEG")  # You can choose the format based on your image type (e.g., JPEG, PNG)
    img_bytes = buffered.getvalue()

    return img_bytes


if __name__ == "__main__":
    # Test the get_classes function
    test_image_path = "C:\\Users\\micha\\Downloads\\test2.jpg"  # Replace with an actual image path
    try:
        detected_image, labels = get_classes(test_image_path)
        print(f"Detected Labels: {labels}")
        # Save or show the detected image for validation
        with open("detected_output.jpg", "wb") as f:
            f.write(detected_image)
        print("Detected image saved as 'detected_output.jpg'")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
