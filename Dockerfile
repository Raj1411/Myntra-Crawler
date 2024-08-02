# Use Python 3.11 slim base image
FROM python:3.11-slim

# Install necessary dependencies and tools
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libatspi2.0-0 \
    libdbus-1-3 \
    libxtst6 \
    libgbm1 \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    && apt-get install -y --fix-broken \
    && rm google-chrome-stable_current_amd64.deb

# Install Chromedriver
RUN wget https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Run the application
CMD ["gunicorn", "app:app"]
