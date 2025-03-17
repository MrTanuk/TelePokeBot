import re
import requests

def getAbility(num_ability):

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

def getDataPokemon(id_pokemon):
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
        abilities[name_ability] = {"data_ability": (getAbility(id_ability)),
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
