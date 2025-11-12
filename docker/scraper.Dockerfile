FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

WORKDIR /scraper

COPY scraper/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade --force-reinstall --no-cache-dir -r /tmp/requirements.txt

COPY scraper/ /scraper/

COPY app/utils /scraper/utils

CMD ["tail", "-f", "/dev/null"]