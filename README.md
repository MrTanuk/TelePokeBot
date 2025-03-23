
# TelePokeBot

A telegram bot that allows to obtain pokemon data and everything related to it, like a pokedex.


## Installation

Need python installed and telegram bot created. Use BotFather.

Create a virtual environment:


```bash
python -m venv env
source /bin/source
```


Install the libraries [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) and [python-dotenv](https://github.com/theskumar/python-dotenv)


```bash
pip install pyTelegramBotAPI python-dotenv
```


Add your bot's token and name in the .env file

```bash
# .env
BOT_TOKEN=
BOT_NAME=
```

Then, can start the bot

```bash
python bot.py
```

Top stop it, use the command Ctrl + C
## Documentation

- Command /pokedex {id/name-pokemon} get the principal data of a pokemon
- Command /help obtain all the commands bot can offers

New features coming soon
