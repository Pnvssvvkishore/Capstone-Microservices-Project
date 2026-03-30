FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m textblob.download_corpora || true
COPY app.py .
EXPOSE 5006
CMD ["python", "app.py"]
