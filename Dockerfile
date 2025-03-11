# Use official Python image
FROM python:3.9

# Set working directory inside container
WORKDIR /app

# Copy all files to container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port if needed
EXPOSE 5000

# Run the application
CMD ["python", "script.py"]
