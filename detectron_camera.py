import cv2
import torch
import torchvision
import detectron2
from detectron2.utils.logger import setup_logger
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
def get_classes(image_path):
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
    ret, jpeg = cv2.imencode('.jpg', detected_frame)
    
    # Return the encoded image and predicted labels
    return jpeg.tobytes(), predicted_labels
