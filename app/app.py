import warnings
warnings.filterwarnings('ignore')

from scripts.data_model import  ImageDataInput, ImageDataOutput
from scripts import s3
from ultralytics import YOLO
from fastapi import FastAPI
from fastapi import Request
import uvicorn
from fastapi.responses import FileResponse
import requests, os, time, uuid
import os
import time
import requests
import base64
import torch



app = FastAPI()

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# ####### Download ML Models ##########

force_download = True # False

model_name = 'yolov11m/'
local_path = 'ml-models/'+model_name
os.makedirs("results", exist_ok=True)

if not os.path.isdir(local_path) or force_download:
    s3.download_dir(local_path, model_name)
detection_model = YOLO(local_path+ "best.pt")


######## Download ENDS  #############


@app.get("/")
def read_root():
    return "Hello! I am up!!!"



@app.post("/api/v1/object_detection")
async def object_detection(data: ImageDataInput):
    start = time.time()
    os.makedirs("images", exist_ok=True)
    image_id = uuid.uuid4().hex
    img_path = f"images/{image_id}.jpg"

    # Download image from first URL (you can extend to multiple later)
    response = requests.get(data.url[0])
    with open(img_path, 'wb') as f:
        f.write(response.content)

    # Run YOLO + save image with bounding boxes
    results =detection_model(img_path)
    result_img_path = f"results/{image_id}.jpg"
    results[0].save(filename= result_img_path)


    # Extract predictions
    boxes = results[0].boxes
    scores = boxes.conf.tolist() if boxes is not None else []

    # Convert image to base64
    with open(result_img_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Clean up
    os.remove(img_path)
    end = time.time()
    prediction_time = int((end - start) * 1000)

    return ImageDataOutput(
        model_name=model_name,
        url=data.url,
        image=[base64_image],  # put base64 image here
        scores=scores,
        prediction_time=prediction_time
    )
