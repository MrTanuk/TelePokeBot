
# TelePokeBot

A telegram bot that allows to obtain pokemon data and everything related to it, like a pokedex.


## Installation

Need python installed and telegram bot created. Use BotFather.

clone the repository:

```bash
git clone git@github.com:MrTanuk/TelePokeBot.git
cd TelePokeBot
```


Create a virtual environment:

```bash
python -m venv env
```


To active the virtual environment:


Linux/macOS:
```bash
source venv/bin/activate
```


Windows:
```bash
.\venv\Scripts\activate
```


Install the libraries [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) and [python-dotenv](https://github.com/theskumar/python-dotenv)

```bash
pip install pyTelegramBotAPI python-dotenv
```

Add your bot's token and name in a .env file. 

```bash
BOT_TOKEN=1234567890
BOT_NAME=name_example
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
