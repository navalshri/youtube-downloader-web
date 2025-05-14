# Use a slim version of Python 3.10 as the base image
FROM python:3.10-slim

# Install ffmpeg (to merge video and audio)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 10000 (Render default port)
EXPOSE 10000

# Run the app
CMD ["python", "app.py"]
