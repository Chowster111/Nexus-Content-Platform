# Use a slim Python base image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Selenium/Chrome (adjust as needed)
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium-browser \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY ../../requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the scraper code
COPY . /app/

# Set environment variables for headless Chrome (if needed)
ENV PYTHONUNBUFFERED=1
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Set the entrypoint to your batch scraper script (replace with your actual script/module)
CMD ["python", "-m", "scraper.batch_entry"] 