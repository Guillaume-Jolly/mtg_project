import os
import json
import time

# Chemin vers le fichier JSON en entrée
input_directory = os.path.join(os.getcwd(), 'Input')
input_json_file_path = os.path.join(input_directory, 'AllPrices.json')  # Utilisation du fichier AllPrices.json

# Obtenir le nom du fichier sans extension
input_file_name = os.path.splitext(os.path.basename(input_json_file_path))[0]

# Chemin vers le répertoire de sortie
output_directory = os.path.join(os.getcwd(), 'Output')
os.makedirs(output_directory, exist_ok=True)  # Crée le répertoire de sortie s'il n'existe pas

# Charger le JSON depuis le fichier en entrée
with open(input_json_file_path, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# Fonction pour obtenir le schéma JSON
def get_json_schema(json_data, parent_name=''):
    schema = {}

    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if parent_name:
                field_name = f"{parent_name}.{key}"
            else:
                field_name = key

            if isinstance(value, dict):
                schema[field_name] = get_json_schema(value, parent_name=field_name)
            elif isinstance(value, list):
                if len(value) > 0 and isinstance(value[0], dict):
                    schema[field_name] = [get_json_schema(value[0], parent_name=field_name)]
                else:
                    schema[field_name] = "List of {}".format(type(value[0]).__name__)
            else:
                schema[field_name] = type(value).__name__

    elif isinstance(json_data, list):
        if len(json_data) > 0 and isinstance(json_data[0], dict):
            schema[parent_name] = [get_json_schema(json_data[0], parent_name=parent_name)]
        else:
            schema[parent_name] = "List of {}".format(type(json_data[0]).__name__)

    return schema

# Obtenir le schéma du JSON
json_schema = get_json_schema(json_data)

# Obtenir un horodatage actuel au format 'YYYYMMDD_HHMMSS'
current_timestamp = time.strftime("%Y%m%d_%H%M%S")

# Nom du fichier de sortie avec le nom du fichier JSON d'entrée et l'horodatage
output_file_name = f"{input_file_name}_{current_timestamp}_schema.json"

# Chemin complet du fichier de sortie
output_schema_file_path = os.path.join(output_directory, output_file_name)

# Écrire le schéma JSON dans le fichier de sortie
with open(output_schema_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(json_schema, output_file, indent=4, ensure_ascii=False)

print(f"Schéma JSON généré et enregistré dans '{output_schema_file_path}'.")
