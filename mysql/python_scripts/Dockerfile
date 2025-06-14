FROM python:3.13-slim

WORKDIR /mysql/python_scripts


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir pymysql cryptography


COPY updater.py .
COPY wait-for-db.sh .

RUN chmod +x ./wait-for-db.sh

ENTRYPOINT ["./wait-for-db.sh"]