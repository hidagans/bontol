FROM nikolaik/python-nodejs:python3.10-nodejs18

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg neofetch git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/hidagans/bontol.git /bontol

WORKDIR /bontol

RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt

CMD ["python3", "-m", "ubot"]
