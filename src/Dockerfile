# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg


# Copy the requirements.txt file to the container
COPY /src/requirements.txt .

# Install the app's dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app to the container
COPY src/ .

CMD streamlit run --server.enableCORS false Home.py
