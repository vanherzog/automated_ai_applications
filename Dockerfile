# Base image for building Python and Node.js
FROM python:3.9-slim as base

# Install Node.js and common dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    unzip \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs \
    && apt-get install -y npm

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Set up working directory for backend and frontend
WORKDIR /app

# Copy Python requirements and install dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install -r backend/requirements.txt

# Copy Node.js frontend dependencies and install
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install

# Copy all source code for backend and frontend
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Copy the Skills_data.docx file
COPY backend/Skills_data.docx ./backend/

# Build React app
RUN cd frontend && npm run build

# Install `serve` to serve the built frontend
RUN npm install -g serve

# Expose ports for frontend (3000) and backend API (5000)
EXPOSE 3000 5000

# Default command will be overridden by each service in docker-compose
CMD ["echo", "Specify a command in docker-compose.yml"]