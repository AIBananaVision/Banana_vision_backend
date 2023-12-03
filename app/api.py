import json
from aws_model import model_infer
import boto3
from fastapi import FastAPI
from typing import Annotated
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import cloudinary_config as cloudinary_config
from cloudinary.uploader import upload
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from fastapi import BackgroundTasks
from fastapi import Depends
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
# Import the File type from models.py
from models import LocationData, ImageUpload
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import httpx
load_dotenv()

app = FastAPI()


# Load the MongoDB URI from the .env file
remote_mongo_db_uri = os.getenv("MONGODB_URI")
port = 8000

client = MongoClient(remote_mongo_db_uri, port)
db = client["BananaVision"]
collection = db["BananaData"]

app = FastAPI(
    title="Backend API for BananaVison",
    description="",
    version="0.1",
)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=['*']
)


def get_location_dependency(location: LocationData = Depends(LocationData)):
    return location


class UploadException(Exception):
    def __init__(self, message="Error during file upload"):
        self.message = message
        super().__init__(self.message)


class SaveImageDataException(Exception):
    def __init__(self, message="Error during saving image data"):
        self.message = message
        super().__init__(self.message)


# Change the definition of save_image_data to remove the incorrect usage of model_infer
async def save_image_data(imageUpload: ImageUpload, model_results: dict):
    try:
        # Your save logic here
        print("Model results: ",model_results)
        disease_class = model_results.get('predicted_class')
        probabilities = model_results.get('probabilities')

        print("Image URL:", imageUpload.image_url)
        print("Location:", imageUpload.location.dict())
        print("Disease Class:", disease_class)
        print("Probabilities:", probabilities)

        document = {
            "image_url": imageUpload.image_url,
            "location": imageUpload.location.dict(),
            "disease_class": disease_class,
            "probabilities": probabilities
        }
        result = collection.insert_one(document)
        print(f"Image data saved with id: {result.inserted_id}")

    except Exception as e:
        raise SaveImageDataException(f"{str(e)}")

# Correct the definition of upload_and_infer to pass the ImageUpload object to model_infer
@app.post("/upload-data")
async def upload_and_infer(
    background_tasks: BackgroundTasks,
    image_file: UploadFile = UploadFile(...),
    location: LocationData = Depends(get_location_dependency)
):
    try:
        # Check if the file is empty
        if not image_file.content_type or image_file.content_type.startswith("text"):
            raise HTTPException(status_code=400, detail="Empty or invalid file")

        # Upload image to Cloudinary
        cloudinary_response = upload(image_file.file, folder="banana-vision")
        # Get the Cloudinary image URL
        image_url = cloudinary_response['secure_url']
        async with httpx.AsyncClient() as client:
            image_response = await client.get(image_url)
            image_content = image_response.content
        # Pass the ImageUpload object to model_infer
        model_results = await model_infer(image_content)

        # Check if the file is empty after reading
        if not model_results:
            raise HTTPException(status_code=500, detail="Empty result from model inference")

        # Add the task to save the image data in the background
        background_tasks.add_task(save_image_data, ImageUpload(
            image_url=image_url,
            location=location
        ), model_results)
        
        return JSONResponse(content={"image_url": image_url, "location": location.dict(),"model_results":model_results})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
