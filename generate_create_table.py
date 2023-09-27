import os
import json

# Chemin vers le fichier JSON
json_file_path = os.path.join('Input', 'AllPrintings.json')

# Charger le JSON
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    mtg_data = json.load(json_file)

# Extrait les informations de structure à partir de la première carte
sample_card = next(iter(mtg_data['data'].values()))  # Prend une carte exemple

# Définir les types de données pour chaque colonne en fonction des données de la carte exemple
column_types = {}
for key, value in sample_card.items():
    if isinstance(value, int):
        column_types[key] = 'INTEGER'
    elif isinstance(value, str):
        column_types[key] = 'VARCHAR(255)'
    else:
        column_types[key] = 'TEXT'

# Génère la commande SQL CREATE TABLE dynamiquement
create_table_query = f"CREATE TABLE IF NOT EXISTS mtg_cards (\n"
for column_name, column_type in column_types.items():
    create_table_query += f"    {column_name} {column_type},\n"
create_table_query = create_table_query.rstrip(',\n')  # Supprime la dernière virgule et le saut de ligne
create_table_query += "\n)"

# Chemin vers le sous-dossier "BDD" pour enregistrer le fichier SQL
output_directory = os.path.join(os.getcwd(), 'BDD')
os.makedirs(output_directory, exist_ok=True)  # Crée le sous-dossier s'il n'existe pas

# Écrit la commande SQL CREATE TABLE dans un fichier dans le sous-dossier "BDD"
sql_file_path = os.path.join(output_directory, 'create_table_mtg_cards.sql')
with open(sql_file_path, 'w', encoding='utf-8') as sql_file:
    sql_file.write(create_table_query)

print(f"Commande SQL CREATE TABLE générée et enregistrée dans '{sql_file_path}'.")

# Exporte le format JSON détecté dans un fichier séparé
json_format_path = os.path.join(output_directory, 'json_format_detected.json')
with open(json_format_path, 'w', encoding='utf-8') as json_format_file:
    json.dump(column_types, json_format_file, indent=4)

print(f"Format JSON détecté enregistré dans '{json_format_path}'.")
