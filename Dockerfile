# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install uv (fast pip replacement)
RUN pip install --no-cache-dir uv

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies with uv
RUN uv pip install --system -r requirements.txt

# Copy all project files into container
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]