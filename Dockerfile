# Use the official Python image as the base image
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the startup script into the container
COPY startup.sh /usr/src/app/startup.sh

# Make the startup script executable
RUN chmod +x /usr/src/app/startup.sh

# Copy the rest of the application files into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Use the startup script as the entry point
CMD ["/usr/src/app/startup.sh"]

