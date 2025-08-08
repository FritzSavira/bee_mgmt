FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:create_app()"]

# Start the Gunicorn server
CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2"]