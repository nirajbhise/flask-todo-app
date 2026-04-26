# Step 1 — Use official Python slim base image
FROM python:3.11-slim
 
# Step 2 — Set working directory inside the container
WORKDIR /app
 
# Step 3 — Copy requirements first (for Docker layer caching)
COPY app/requirements.txt .
 
# Step 4 — Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
 
# Step 5 — Copy the rest of the application code
COPY app/ .
 
# Step 6 — Create non-root user (Linux security best practice)
RUN mkdir -p /data && \
    adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /data /app
 
# Step 7 — Switch to non-root user
USER appuser
 
# Step 8 — Expose port 5000
EXPOSE 5000
 
# Step 9 — Command to run the application
CMD ["python", "app.py"]

