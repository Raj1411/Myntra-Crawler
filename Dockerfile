FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -fy \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    && apt-get -fy install \
    && rm google-chrome-stable_current_amd64.deb

# Install Chromedriver
RUN wget https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Install Python packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app
WORKDIR /app

# Run the application
CMD ["gunicorn", "app:app"]
