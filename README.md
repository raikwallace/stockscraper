# Stockscraper Bot

> Telegram bot for stock status notifications.

![Docker Image Version (tag latest semver)](https://img.shields.io/docker/v/raikwallace/stockscraperbot/latest?label=docker%20image)

This bot can search for stock at the NVIDIA official's store, to find Founder's Edition graphic cards. It uses scrapy with splash to navigate for NVIDIA's web. The scrapy's spiders are controlled by a Telegram bot that can start new spiders, manage notification lists and send those notifications.

## Prerequisites

The project is developed in Python 3.7.3.

To run telegram bot you need to ask for a token to @BotFather.

The following libraries are needed:

```sh
python -m pip install python-telegram-bot
python -m pip install scrapy
python -m pip install scrapy-splash
python -m pip install scrapyscript
```

## Usage example

For run bot in local is needed a splash server running.

```sh
docker run -p 8050:8050 scrapinghub/splash
python bot.py
```

With docker, just run:

```sh
docker compose up
```

## Meta

Daniel "Raik Wallace" López – [@RaikWallace](https://twitter.com/raikwallace) – raik@67gam.es

Distributed under the XYZ license. See `LICENSE` for more information.

[https://github.com/raikwallace](https://github.com/raikwallace/)

## Contributing

1. Fork it (<https://github.com/raikwallace/stockscraper/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
