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


async def save_image_data(imageUpload: ImageUpload):
    try:
        # Your save logic here
        print("Image URL: ", imageUpload.image_url)
        print("Location: ", imageUpload.location.dict())
        document = {
            "image_url": imageUpload.image_url,
            "location": imageUpload.location.dict(),
            "disease_class": "healthy"
        }
        result = collection.insert_one(document)
        print(f"Image data saved with id: {result.inserted_id}")

    except Exception as e:
        raise SaveImageDataException(f"{str(e)}")


@app.post("/upload-data")
async def upload_and_infer(background_tasks: BackgroundTasks, file: UploadFile = UploadFile(...), location: LocationData = Depends(get_location_dependency)):
    try:
       
        model_results = await model_infer(file)
        print("Model results: ",model_results)
        # Upload image to Cloudinary
        cloudinary_response = upload(file.file, folder="banana-vision")

        # Get the Cloudinary image URL
        image_url = cloudinary_response['secure_url']

        # Add the task to save the image data in the background
        background_tasks.add_task(save_image_data, ImageUpload(
            image_url=image_url, location=location))

        # Return the response without awaiting the background task
        return JSONResponse(content={"image_url": image_url, "location": location.dict()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
