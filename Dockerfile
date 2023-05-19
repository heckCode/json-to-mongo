# Use an official Python runtime as a parent image
FROM python:3.9-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Specify the path within the container to access the mapped files
ENV MAPPED_FILES_DIR /mapped_files

# Create the directory for mapped files
RUN mkdir $MAPPED_FILES_DIR

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run your_script.py when the container launches, replace 'your_script.py' with your actual python script filename
CMD ["python", "insert-to-mongo.py"]