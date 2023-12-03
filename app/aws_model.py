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

# Initializing a SageMaker runtime client with region
client = boto3.client('sagemaker-runtime', region_name=region_name)

#  SageMaker endpoint name
endpoint_name = 'pytorch-inference-2023-12-02-22-34-19-675'  

async def model_infer(image_content):
    try:
        print("Uploading image to AWS server...............")
       
        
        # Inference request
        response = client.invoke_endpoint(
            EndpointName=endpoint_name,
            Body=image_content,
            ContentType='application/x-image',
            Accept='application/json'
        )

        # Parsing the response
        result = json.loads(response['Body'].read().decode())
        formatted_result = {
            'predicted_class': result.get('predicted_class', 'Unknown'),
            'probabilities': result.get('probabilities', {})
        }
        print(formatted_result)

        return formatted_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


