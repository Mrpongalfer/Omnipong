# Use a base Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project files
COPY . .

# Set the entry point
CMD ["python", "main.py"]

