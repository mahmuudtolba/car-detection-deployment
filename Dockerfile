FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --upgrade pip \
    && pip install --timeout 3000 --retries 10 -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
