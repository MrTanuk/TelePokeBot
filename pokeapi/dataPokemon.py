import re
import requests

def obtainDatasAbility(num_ability):

    url = f'https://pokeapi.co/api/v2/ability/{num_ability}/'
    data_ability = requests.get(url).json()
    results_abilities = {}

    if len(data_ability["effect_entries"]) != 0:
        for effect in reversed(data_ability["effect_entries"]):
            if effect["language"]["name"] == "en":
                results_abilities["effect"] = effect["effect"]
                results_abilities["short_effect"] = effect["short_effect"]
                break
    else:
        for effect in reversed(data_ability["flavor_text_entries"]):
            if effect["language"]["name"] == "en":
                results_abilities["effect"] = effect["flavor_text"]
                results_abilities["short_effect"] = "No data"
    return results_abilities

def obtainDatasPokemon(id_pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon-species/{id_pokemon}/'
    general_data  = requests.get(url)

    if not general_data:
        return False

    data = general_data.json()
    
    name_pokemon = data["name"]
    id = data["id"]
    character_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}").json()
    url_sprite = character_data["sprites"]["front_default"]
    
    types = []
    for name_types in character_data["types"]:
        types.append(name_types["type"]["name"])

    specie = {}
    for some_genus in data["genera"]:
        if some_genus["language"]["name"] in ["en"]:
            specie["name_specie"] = some_genus["genus"]
            break

    for some_description in reversed(data["flavor_text_entries"]):
        if some_description["language"]["name"]  == "en":
            specie["description"] = some_description["flavor_text"]
            break

    weight = character_data["weight"]/10
    height = character_data["height"]/10

    abilities = {}
    for ability in character_data["abilities"]:
        name_ability = ability["ability"]["name"]
        id_ability = (re.findall(r'\d+', ability["ability"]["url"])[-1])
        abilities[name_ability] = {"data_ability": (obtainDatasAbility(id_ability)),
                                   "is_hidden": ability["is_hidden"]}

    stats = {}
    for stat in character_data["stats"]:
        stats[stat["stat"]["name"]] = stat["base_stat"]

    return {"id": id,
            "image": url_sprite,
            "name": name_pokemon,
            "type": types,
            "specie": specie,
            "weight": weight,
            "height": height,
            "ability": abilities,
            "stats": stats,
    }

def getPokemon(pokemon):
    data_pokemon = obtainDatasPokemon(pokemon)

    if not data_pokemon:
        return None

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
    return {"data": all_data_pokemon, "image" : data_pokemon["image"]}

pikachu = getPokemon(25)
