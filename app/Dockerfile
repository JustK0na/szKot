FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libcairo2-dev \
        libcups2-dev \
        python3 \
        python3-dev \
        default-libmysqlclient-dev \
        build-essential \
        libjpeg-dev \
        zlib1g-dev \
        libpng-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libopenjp2-7-dev \
        libtiff-dev \
        libwebp-dev \
        tcl8.6-dev \
        tk8.6-dev \
        python3-tk \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


ENV AM_I_IN_A_DOCKER_CONTAINER=Yes

COPY . .

ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000


CMD ["flask", "run"]