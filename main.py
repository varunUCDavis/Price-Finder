'''
Identifies individual hats from given hat lot images
'''
import io
import cv2
from PIL import Image
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import yaml
import numpy as np
import os
from getLots import Lots
from priceFinder import PriceFinder
from pdfGen import GenPDF

with open("config.yaml", 'r') as file:
    config = yaml.safe_load(file)

# get hat lot images
lot_dict = Lots.getLots()

# model path
model_path = config['path']+config['model_path']
model = YOLO(model_path)

# 2d list to hold cropped hat images for each hat lot image
data = []

lot_names = list(lot_dict.keys())
values = list(lot_dict.values())
images = [item[0] for item in values]
links = [item[1] for item in values]
lot_prices = [item[2] for item in values]
#breakpoint()
results = model.predict(source=images)
for r,image,link,lot_price in zip(results,images,links,lot_prices):
    hats = []
    image = np.ascontiguousarray(np.array(image))
    annotator = Annotator(image)
    image = Image.fromarray(image)
    boxes = r.boxes
    num_hats = len(boxes)
    for box in boxes:
        conf = box.conf.item() # Convert tensor to float
        if conf > 0.65: # Check if confidence is greater than 65%
            b = box.xyxy[0].tolist() # get box coordinates in (left, top, right, bottom) format
            c = box.cls
            label = f'{model.names[int(c)]} {conf:.2f}' # Combine class name and confidence score
            annotator.box_label(b, label) # Add the label to the box only if conf > 65%
            # Cropping the image
            cropped_image = image.crop((b[0], b[1], b[2], b[3]))  # Pillow uses (left, upper, right, lower)
            img_byte_arr = io.BytesIO()
            # Save image to the bytes buffer using a format (e.g., JPEG, PNG)
            cropped_image.save(img_byte_arr, format='JPEG')
            # Get the byte value of the image
            tmp = img_byte_arr.getvalue()
            
            # get price for individual hat
            price = PriceFinder.find_prices(tmp)
            hats.append([cropped_image,price])
    if len(hats) > 0:
        data.append([image, num_hats, link, hats, lot_price])
#breakpoint()
GenPDF.generatePDF(data)




