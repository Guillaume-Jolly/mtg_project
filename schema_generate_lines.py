import os
import jsonlines
import json
import time

# Chemin vers le fichier JSON
json_file_path = os.path.join('Input', 'CardTypes.json')

# Charger le JSON
start_time = time.time()

with jsonlines.open(json_file_path) as reader:
    for obj in reader:
        # Extrait les informations de structure à partir de la première carte
        sample_card = next(iter(obj['data'].values()))  # Prend une carte exemple

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

        # Écrit la commande SQL dans un fichier dans le sous-dossier "BDD"
        timestamp = int(time.time())
        sql_file_path = os.path.join(output_directory, f'create_table_mtg_cards_{timestamp}.sql')
        with open(sql_file_path, 'w', encoding='utf-8') as sql_file:
            sql_file.write(create_table_query)

        print(f"Commande SQL CREATE TABLE générée et enregistrée dans '{sql_file_path}'.")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Temps écoulé : {elapsed_time} secondes")
