# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app


# Copy the requirements.txt file to the container
COPY /src/requirements.txt .

# Install the app's dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app to the container
COPY src/ .

CMD streamlit run --server.port 8080 --server.enableCORS false Home.py
