# Use a Python base image
FROM python:3.11-slim

# Install necessary dependencies and tools
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
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

# Add Google Chrome's GPG key
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add -

# Add Google Chrome repository
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'

# Install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# Copy ChromeDriver from the repository into the image
COPY drivers/chromedriver /usr/local/bin/chromedriver
RUN chmod +x /usr/local/bin/chromedriver

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run the application
CMD ["gunicorn", "app:app"]
