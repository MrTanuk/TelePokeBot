import re
import requests
from requests.exceptions import RequestException, HTTPError

def fetchData(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    except HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPError("Pokémon not found")
        raise HTTPError("Server error. Try later.")

    except RequestException:
        raise RequestException("Connection error. Try later.")

def obtainDatasAbility(num_ability):
    try:
        data_ability = fetchData(f"https://pokeapi.co/api/v2/ability/{num_ability}/")
    except RequestException:
        raise RequestException(f"Error obtain ability: Connection error, try later.")

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
                results_abilities["short_effect"] = "no data"
    return results_abilities

def obtainDatasPokemon(pokemon):
    try:
        species_data = fetchData(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}/")
        pokemon_data = fetchData(f"https://pokeapi.co/api/v2/pokemon/{species_data['id']}/")
    except (HTTPError, RequestException) as e:
        raise e

    # formatting data
    name_pokemon = species_data["name"]
    url_sprite = pokemon_data["sprites"]["front_default"]
    
    types = [t["type"]["name"] for t in pokemon_data["types"]]

    # obtain gender and description
    specie = {}
    for genus in species_data["genera"]:
        if genus["language"]["name"] == "en":
            specie["name_specie"] = genus["genus"]
            break

    for entry in reversed(species_data["flavor_text_entries"]):
        if entry["language"]["name"] == "en":
            specie["description"] = entry["flavor_text"].replace("\n", " ")
            break

    # getting abilities
    abilities = {}
    for ability in pokemon_data["abilities"]:
        name_ability = ability["ability"]["name"]
        ability_url = ability["ability"]["url"]
        id_ability = re.findall(r'\d+', ability_url)[-1]
        
        try:
            ability_data = obtainDatasAbility(id_ability)
        except RequestException as e:
            raise 
        
        abilities[name_ability] = {
            "data_ability": ability_data,
            "is_hidden": ability["is_hidden"]
        }

    return {
        "id": pokemon_data["id"],
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
    except Exception as e:
        return {"error": f"{e}"}

    #a formatting data to telegram message 
    types = " ".join(data_pokemon["type"])
    
    abilities = "\n".join([
        f"{name} - {'hidden' if data['is_hidden'] else 'not hidden'}"
        for name, data in data_pokemon["ability"].items()
    ])

    return {
        "data": f"""
<strong>id:</strong> {data_pokemon['id']}
<strong>name:</strong> {data_pokemon['name']}
<strong>type:</strong> {types}
<strong>ability:</strong>\n{abilities}
<strong>specie:</strong> {data_pokemon['specie']['name_specie']}
<strong>description:</strong> {data_pokemon['specie']['description']}
<strong>weight:</strong> {data_pokemon["weight"]} kg
<strong>height:</strong> {data_pokemon["height"]} m
        """,
        "image": data_pokemon["image"]
    }
