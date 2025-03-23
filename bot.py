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
        return

    pokemon_id = message.text.split()[1]
    pokemon_data = getPokemon(pokemon_id)
    if "error" in pokemon_data:
        bot.send_message(message.chat.id, f"{pokemon_data['error']}")
        return None

    url_image = pokemon_data["image"]
    pokemon_data = pokemon_data["data"]

    bot.send_photo(message.chat.id, url_image, pokemon_data, parse_mode="HTML")

@bot.message_handler(commands=["help", f"help@{BOT_NAME}"], chat_types=["private", "group","supergroup"])
def send_help(message):

    help_text = """
    Commands available
    <code>/pokedex</code> - Search information about a Pokemon
    """
    bot.send_message(message.chat.id, help_text, parse_mode="HTML")

bot.infinity_polling()
