# Use a pre-built Selenium image with Chrome
FROM selenium/standalone-chrome:latest

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Run the application
CMD ["gunicorn", "app:app"]
