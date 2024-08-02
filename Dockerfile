FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Download and install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN apt-get -fy install

# Download and install Chromedriver
RUN wget https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/local/bin/chromedriver

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Python script
COPY . /app
WORKDIR /app

CMD ["python", "app.py"]
