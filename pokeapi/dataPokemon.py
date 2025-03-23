import re
import requests
from requests.exceptions import RequestException

def obtainDatasAbility(num_ability):
    url = f'https://pokeapi.co/api/v2/ability/{num_ability}/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data_ability = response.json()
    except RequestException as e:
        raise RequestException(f"Error fetching ability data: {e}")

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
    try:
        # Specie datas
        species_url = f'https://pokeapi.co/api/v2/pokemon-species/{id_pokemon}/'
        species_response = requests.get(species_url)
        species_response.raise_for_status()
        species_data = species_response.json()
        
        # Pokemon datas
        pokemon_id = species_data["id"]
        pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
        pokemon_response = requests.get(pokemon_url)
        pokemon_response.raise_for_status()
        pokemon_data = pokemon_response.json()
        
    except RequestException as e:
        raise RequestException(f"Error fetching Pokemon data: {e}")

    # Formatting data
    name_pokemon = species_data["name"]
    url_sprite = pokemon_data["sprites"]["front_default"]
    
    types = [t["type"]["name"] for t in pokemon_data["types"]]

    # Obtain gender and description
    specie = {}
    for genus in species_data["genera"]:
        if genus["language"]["name"] == "en":
            specie["name_specie"] = genus["genus"]
            break

    for entry in reversed(species_data["flavor_text_entries"]):
        if entry["language"]["name"] == "en":
            specie["description"] = entry["flavor_text"].replace("\n", " ")
            break

    # Getting abilities
    abilities = {}
    for ability in pokemon_data["abilities"]:
        name_ability = ability["ability"]["name"]
        ability_url = ability["ability"]["url"]
        id_ability = re.findall(r'\d+', ability_url)[-1]
        
        try:
            ability_data = obtainDatasAbility(id_ability)
        except RequestException as e:
            raise RequestException(f"Error en habilidad {name_ability}: {e}")
        
        abilities[name_ability] = {
            "data_ability": ability_data,
            "is_hidden": ability["is_hidden"]
        }

    return {
        "id": pokemon_id,
        "image": url_sprite,
        "name": name_pokemon,
        "type": types,
        "specie": specie,
        "weight": pokemon_data["weight"]/10,
        "height": pokemon_data["height"]/10,
        "ability": abilities,
        "stats": {s["stat"]["name"]: s["base_stat"] for s in pokemon_data["stats"]}
    }

def getPokemon(pokemon):
    try:
        data_pokemon = obtainDatasPokemon(pokemon)
    except RequestException as e:
        return {
            "error": "⚠️Erro on server. Please, try later"
        }
    except Exception as e:
        return {
            "error": f"Error: {str(e)}"
        }

    # Formatear la respuesta
    types = " ".join(data_pokemon["type"])
    
    abilities = "\n".join([
        f"{name} - {'hidden' if data['is_hidden'] else 'not hidden'}"
        for name, data in data_pokemon["ability"].items()
    ])

    return {
        "data": f"""
<strong>ID:</strong> {data_pokemon['id']}
<strong>Name:</strong> {data_pokemon['name']}
<strong>Type:</strong> {types}
<strong>Ability:</strong>\n{abilities}
<strong>Specie:</strong> {data_pokemon['specie']['name_specie']}
<strong>Description:</strong> {data_pokemon['specie']['description']}
<strong>Weight:</strong> {data_pokemon["weight"]} kg
<strong>Height:</strong> {data_pokemon["height"]} m
        """,
        "image": data_pokemon["image"]
    }
