import os
from dotenv import load_dotenv
import telebot
from pokeapi.dataPokemon import getPokemon

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
BOT_NAME = str(os.getenv("BOT_NAME"))

bot = telebot.TeleBot(BOT_TOKEN)
bot.set_my_commands([
    telebot.types.BotCommand("/help", "Show all the commands"),
    telebot.types.BotCommand("/pokedex", "Search information about a Pokemon"),
])

@bot.message_handler(commands=["pokedex", f"pokedex@{BOT_NAME}"], chat_types=["private", "group", "supergroup"])
def find_pokemon(message):

    if len(message.text.split()) == 1:
        text_use_command = """
Type name or ID of the pokemon:
    <code>/pokedex pikachu</code>
    <code>/pokedex 25</code> 
"""
        bot.send_message(message.chat.id, text_use_command, parse_mode="HTML")
        return None

    id_pokemon = message.text.split()[1]
    data_pokemon = getPokemon(id_pokemon)
    if not data_pokemon:
        bot.send_message(message.chat.id, "Pokemon not found. Try again")
        return None
    
    url_image = data_pokemon["image"]
    data_pokemon = data_pokemon["data"]

    bot.send_photo(message.chat.id, url_image, data_pokemon, parse_mode="HTML")

@bot.message_handler(commands=["help", f"help@{BOT_NAME}"], chat_types=["private", "group","supergroup"])
def send_help(message):

    help_text = """
    Commands available
    <code>/pokedex</code> - Search information about a Pokemon
    """
    bot.send_message(message.chat.id, help_text, parse_mode="HTML")

bot.infinity_polling()
