from PIL import Image
import io
import boto3
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure AWS credentials using environment variables
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("REGION_NAME")

# Initializing a SageMaker runtime client with region
client = boto3.client('sagemaker-runtime', region_name=region_name)

# Load your image
image_path = './../Images/Image_2826.jpg'
with open(image_path, 'rb') as f:
    payload = f.read()

# SageMaker endpoint name
endpoint_name = 'pytorch-inference-2023-12-02-22-34-19-675'

# Inference request
response = client.invoke_endpoint(
    EndpointName=endpoint_name,
    Body=payload,
    ContentType='application/x-image',
    Accept='application/json'
)

# Parsing the response
result = json.loads(response['Body'].read().decode())
print(result)
