# Use the official Python image as the base image for building
FROM python:3.9-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Add .env file
COPY .env .

# Copy the entire project directory to the container
COPY . .

# Use a smaller base image for the final image
FROM python:3.9-slim

WORKDIR /app

# Copy only necessary files from the builder stage
COPY --from=builder /app .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]


