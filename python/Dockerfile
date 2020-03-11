FROM nginx/unit:1.14.0-python3.7
WORKDIR /usr/src/app
COPY blog .
RUN apt update && apt install -y python3-pip                               \
    && pip3 install -r ./requirements.txt                            \
    && rm -rf /var/lib/apt/lists/* 