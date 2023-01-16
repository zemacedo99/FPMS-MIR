# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app
# Copy the rest of the application code into the container
# COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt


# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the command to start the app
CMD ["python3", "app.py"]
