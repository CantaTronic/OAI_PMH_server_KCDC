FROM python:3.10
EXPOSE 8000
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD touch .env
CMD uvicorn main:app --host 0.0.0.0 --port 8000
