FROM python:3.11-slim

WORKDIR /app 

COPY ./app /app 

RUN pip install --timeout 3000 --retries 10 -r requirements.txt

CMD ["uvicorn"  , "app:app" , "--host"  , "0.0.0.0" , "--port" , "5000"]