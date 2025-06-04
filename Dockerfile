FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y wget unzip fonts-liberation libnss3 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 libdbus-glib-1-2 && \
    rm -rf /var/lib/apt/lists/*

# Install chrome-headless-shell
RUN wget -q -O /tmp/chrome-headless-shell.zip https://storage.googleapis.com/chrome-for-testing-public/latest/linux64/chrome-headless-shell-linux64.zip && \
    unzip -q /tmp/chrome-headless-shell.zip -d /opt/chrome && \
    mv /opt/chrome/chrome-headless-shell-linux64/chrome-headless-shell /usr/bin/ && \
    rm -rf /opt/chrome /tmp/chrome-headless-shell.zip

ENV CHROME_BINARY=/usr/bin/chrome-headless-shell

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "main_withlog.py"]
