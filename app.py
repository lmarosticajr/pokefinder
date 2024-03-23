from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

#=========================================== POKEMON TYPE BY NAME =======================================
def get_pokemon_info(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        pokemon_info = {
            "name": data["name"],
            "id": data["id"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]]
        }
        return pokemon_info
    else:
        return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pokemon', methods=['POST'])
def get_pokemon():
    pokemon_name = request.form['pokemon_name']
    pokemon_info = get_pokemon_info(pokemon_name)
    if pokemon_info:
        return render_template('pokemon.html', pokemon_info=pokemon_info)
    else:
        return "Pokemon não encontrado."
    
#============================== END POKEMON TYPE BY NAME ================================
    
#=========================================== RANDOM POKEMON BY TYPE ==================================== 
def get_random_pokemon_by_type(pokemon_type):
    url = f"https://pokeapi.co/api/v2/type/{pokemon_type.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pokemon_names = [pokemon['pokemon']['name'] for pokemon in data['pokemon']]
        random_pokemon_name = random.choice(pokemon_names)
        return random_pokemon_name
    else:
        return None
    
@app.route('/random_pokemon')
def random_pokemon():
    pokemon_type = request.args.get('type')
    if pokemon_type:
        random_pokemon_name = get_random_pokemon_by_type(pokemon_type)
        if random_pokemon_name:
            return render_template('random_pokemon.html', random_pokemon_name=random_pokemon_name)
        else:
            return "Tipo de Pokémon inválido."
    else:
        return "Por favor, forneça o tipo de Pokémon na consulta."

#========================================== END RANDOM POKEMON BY TYPE ================================= 
    
#========================================= LONGEST NAME BY TYPE =====================================
def get_longest_pokemon_name_by_type(pokemon_type):
    url = f"https://pokeapi.co/api/v2/type/{pokemon_type.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        longest_name = ''
        for pokemon in data['pokemon']:
            pokemon_name = pokemon['pokemon']['name']
            if len(pokemon_name) > len(longest_name):
                longest_name = pokemon_name
        return longest_name
    else:
        return None
    
@app.route('/longest')
def longest_pokemon():
    pokemon_type = request.args.get('type')
    if pokemon_type:
        longest_name = get_longest_pokemon_name_by_type(pokemon_type)
        if longest_name:
            return render_template('longest.html', longest_name=longest_name)
        else:
            return "Tipo de Pokémon inválido."
    else:
        return "Por favor, forneça o tipo de Pokémon na consulta."
#======================================== END OF LONGEST NAME BY TYPE ==============================
if __name__ == '__main__':
    app.run(debug=True)