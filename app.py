from flask import Flask, render_template, request, jsonify, make_response, session
from datetime import datetime, timedelta, timezone
from functools import wraps
import jwt
import requests
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = 'adiuhasiduhasdgahd'
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


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request/args.get('token')
        if not token:
            return jsonify({'Alert':'Token is missing'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except: 
            return jsonify({'Alert':'invalid token'})
    return decorated

@app.route('/public')
def public():
    return 'For Public'

@app.route('/auth')
@token_required
def auth():
    return render_template('search.html')



@app.route('/')
def home():
    if not session.get('logged in'):
        return render_template('login.html')
    else:
        return 'Logged in currently'

@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True
        token = jwt.encode({
            'user':request.form['username'],
            'expiration': str(datetime.now(timezone.utc) + timedelta(seconds=120))
        },
        app.config['SECRET_KEY'])
        return render_template('search.html')

    else:
        return make_response('Unable to verify', 403,{'WWW-Authenticate':'Basic realm: Authentication Failed!'})

@app.route('/search')
def index():
    return render_template('search.html')

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