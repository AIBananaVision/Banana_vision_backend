import boto3
import json
from PIL import Image
import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
load_dotenv()

# Configure AWS credentials using environment variables
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("REGION_NAME")

# Initializing a SageMaker runtime client
client = boto3.client('sagemaker-runtime',region_name=region_name,aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

#  SageMaker endpoint name
endpoint_name = 'pytorch-inference-2023-12-02-22-34-19-675'  

async def model_infer(image: UploadFile):
    try:
        print("Uploading image to AWS server...............")
        # Read image content
        content = await image.read()
        
        # Inference request
        response = client.invoke_endpoint(
            EndpointName=endpoint_name,
            Body=content,
            ContentType='application/x-image',
            Accept='application/json'
        )

        # Parsing the response
        result = json.loads(response['Body'].read().decode())
        print(result)
        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


