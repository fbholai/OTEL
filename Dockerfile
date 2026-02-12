FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY test.py .
ENV OTEL_SERVICE_NAME=pyapp
CMD ["python", "test.py"]