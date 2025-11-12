FROM python:3.11-slim

WORKDIR /analisis-de-bolsa

COPY app/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY app/ ./app

CMD ["tail", "-f", "/dev/null"]