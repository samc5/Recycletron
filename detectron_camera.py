import cv2
import torch
import torchvision
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

        self.cfg = get_cfg()
        # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
        # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        self.cfg.MODEL.DEVICE = "cpu"
        self.predictor = DefaultPredictor(self.cfg)

    def __del__(self):
        self.video.release()        

    def get_frame(self):
        ret, frame = self.video.read()

        # Perform detection on the frame
        outputs = self.predictor(frame)

        # Visualize the predictions
        v = Visualizer(frame[:, :, ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.2)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

        # Convert the output frame back to BGR format for OpenCV
        detected_frame = out.get_image()[:, :, ::-1]

        instances = outputs["instances"].to("cpu")  # Move instances to CPU for easier handling
        predicted_classes = instances.pred_classes.numpy()

        # Get metadata for COCO dataset
        metadata = MetadataCatalog.get("coco_2017_train")

        # Access class names
        class_names = metadata.thing_classes  # This will get the class names in the COCO dataset
        predicted_labels = [class_names[i] for i in predicted_classes]

        print(predicted_labels)

        # Encode the frame as JPEG
        ret, jpeg = cv2.imencode('.jpg', detected_frame)
        return jpeg.tobytes()
