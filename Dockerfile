FROM debian:10-slim
RUN apt-get update && apt-get upgrade -y
RUN apt install htop git build-essential cmake --yes
RUN apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
RUN apt install -y python3 python3-pip
RUN pip3 install python-telegram-bot
RUN pip3 install scrapy
RUN pip3 install scrapyscript
RUN pip3 install scrapy_splash
COPY . /home/stockscraper
ENTRYPOINT python3 /home/stockscraper/bot.py