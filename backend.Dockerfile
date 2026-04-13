# 1. Use an official Python image
FROM python:3.11-slim

# 2. Set the directory inside the container where our code will live
WORKDIR /app

# 3. Copy our requirements file first (this makes building faster)
COPY requirements.txt .

# 4. Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of our application code
COPY . .

# 6. Tell the container to run Uvicorn when it starts
CMD ["python3", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]