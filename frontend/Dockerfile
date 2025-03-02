# Use a lightweight Python image as the base
FROM python:3.11-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies needed for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment to reduce dependencies footprint
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only the necessary files first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the Streamlit port
EXPOSE 8080

# Run Streamlit app
CMD ["streamlit", "run", "llm_benchmark_dashboard.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
