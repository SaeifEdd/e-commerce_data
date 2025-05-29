FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY tests/ tests/
COPY pipeline.py .

CMD ["python", "-m", "unittest", "discover", "tests"]
