import json

# Charger le JSON depuis le fichier d'entrée
input_json_file = 'C:/Users/GuillaumeJOLLY/Documents/mtg_projet/Input/AllPrices.json'
with open(input_json_file, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# Fonction pour aplatir le JSON
def flatten_json(data):
    def _flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                _flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                _flatten(a, name + str(i) + '_')
                i += 1
        else:
            flat_data[name[:-1]] = x

    flat_data = {}
    _flatten(data)
    return flat_data

# Aplatir le JSON
flattened_data = flatten_json(json_data)

# Écrire le JSON aplati dans un fichier de sortie
output_json_file = 'C:/Users/GuillaumeJOLLY/Documents/mtg_projet/Output/AllPricesToday_aplati.json'
with open(output_json_file, 'w', encoding='utf-8') as output_file:
    json.dump(flattened_data, output_file, ensure_ascii=False, indent=4)

print(f"Les données ont été aplaties et enregistrées dans {output_json_file}")
