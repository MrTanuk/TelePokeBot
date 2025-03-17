import os
from dotenv import load_dotenv
import telebot
from pokeapi.pokeapi import getDataPokemon

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
name_bot = ""

bot = telebot.TeleBot(BOT_TOKEN)
bot.set_my_commands([
    telebot.types.BotCommand("/help", "Show all the commands"),
    telebot.types.BotCommand("/pokedex", "Search information about a Pokemon"),
])

@bot.message_handler(commands=["pokedex", f"pokedex@{name_bot}"], chat_types=["private", "group", "supergroup"])
def find_pokemon(message):

    if len(message.text.split()) == 1:
        text_use_command = """
Type name or ID of the pokemon:
    <code>/pokedex pikachu</code>
    <code>/pokedex 25</code> 
"""
        bot.send_message(message.chat.id, text_use_command, parse_mode="HTML")
        return

    id_pokemon = message.text.split()[1]
    data_pokemon = getDataPokemon(id_pokemon)
    if not data_pokemon:
        bot.send_message(message.chat.id, "Pokemon not found. Try again")
        return

    url_image = data_pokemon["image"]

    types = ""
    for name_type in data_pokemon["type"]:
        types += name_type + " "

    abilities = ""    
    for name_ability, data_abilities in data_pokemon["ability"].items():
        abilities +=  name_ability + " - "
        if data_abilities["is_hidden"]:
            abilities += "hidden" + "\n"
        else:
            abilities += "not hidden" + "\n"
    abilities = abilities[:-1]

    all_data_pokemon = f"""
<strong>ID:</strong> {data_pokemon['id']}
<strong>Name:</strong> {data_pokemon['name']}
<strong>Type:</strong> {types}
<strong>Ability:</strong>
{abilities}
<strong>Specie:</strong> {data_pokemon['specie']['name_specie']}
<strong>Description:</strong> {data_pokemon['specie']['description']}
<strong>Weight:</strong> {data_pokemon["weight"]} kg
<strong>Height:</strong> {data_pokemon["height"]} m
"""

    bot.send_photo(message.chat.id, url_image, all_data_pokemon, parse_mode="HTML")

@bot.message_handler(commands=["help", f"help@{name_bot}"], chat_types=["private", "group","supergroup"])
def send_help(message):

    help_text = """
    Commands available
    <code>/pokedex</code> - Search information about a Pokemon
    """
    bot.send_message(message.chat.id, help_text, parse_mode="HTML")

bot.infinity_polling()
