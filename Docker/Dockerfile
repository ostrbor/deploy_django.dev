FROM python:3

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "queue/producer_test.py"]
