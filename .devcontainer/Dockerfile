# Use the official Python image as base
FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# Install system dependencies for WeasyPrint PDF generation
RUN apt-get update && \
    echo "Searching for pango packages..." && \
    apt-cache search libpango && \
    echo "Installing pango packages..." && \
    apt-get install -y libpango-1.0-0 && \
    echo "Installing other dependencies..." && \
    apt-get install -y \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoxft-1.0-0 \
    libharfbuzz0b \
    libfontconfig1 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "Verifying installation..." \
    && dpkg -l | grep pango \
    && echo "Checking library files..." \
    && find /usr/lib -name "*pango*" -type f 2>/dev/null || echo "No pango library files found"

# Set the working directory
WORKDIR /workspaces/BooNooNooNouS

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Switch to non-root user
USER vscode

