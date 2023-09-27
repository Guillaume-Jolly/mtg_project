import os
import psycopg2
import json
from datetime import datetime

# Informations de connexion à la base de données PostgreSQL
db_params = {
    'host': 'localhost',
    'database': 'mtg',
    'user': 'g_jolly',
    'password': 'Production202306!'
}

# Chemin vers le fichier SQL
sql_file_path = os.path.join('BDD', 'create_table_mtg_cards.sql')

# Chemin vers le fichier JSON
json_file_path = os.path.join('Input', 'AllPrintings.json')

# Chemin vers le fichier JSON de format détecté
json_format_path = os.path.join('BDD', 'json_format_detected.json')

# Fonction pour créer la table avec la structure du fichier SQL
def create_table_with_structure(cursor):
    with open(sql_file_path, 'r', encoding='utf-8') as sql_file:
        create_table_query = sql_file.read()
        try:
            cursor.execute(create_table_query)
            print("Table mtg_cards créée avec succès.")
        except Exception as create_error:
            print(f"Erreur lors de la création de la table : {create_error}")

# Fonction pour insérer les données JSON avec le format détecté
def insert_data_with_format(cursor, json_data, json_format):
    try:
        for card_name, card_data in json_data['data'].items():
            insert_query = f"INSERT INTO mtg_cards ({', '.join(json_format.keys())}, dt_creation_date) VALUES ({', '.join(['%s'] * len(json_format.keys()))}, %s)"
            try:
                cursor.execute(insert_query, [card_data.get(key, '') for key in json_format.keys()] + [datetime.now()])
                print(f"Donnée insérée avec succès : {card_name}")
            except Exception as insert_error:
                print(f"Erreur lors de l'insertion des données pour la carte '{card_name}': {insert_error}")
        print("Toutes les données ont été insérées avec succès dans la table mtg_cards.")
    except Exception as insert_error:
        print(f"Erreur générale lors de l'insertion des données : {insert_error}")


try:
    # Établir une connexion à la base de données
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # Supprimer la table mtg_cards et ses dépendances si elle existe déjà
    cursor.execute("DROP TABLE IF EXISTS mtg_cards CASCADE")

    # Créer la table avec la structure du fichier SQL
    create_table_with_structure(cursor)

    # Charger le JSON
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        mtg_data = json.load(json_file)

    # Charger le format JSON détecté
    with open(json_format_path, 'r', encoding='utf-8') as json_format_file:
        json_format = json.load(json_format_file)

    # Insérer les données JSON avec le format détecté
    insert_data_with_format(cursor, mtg_data, json_format)

    # Valider les modifications dans la base de données
    connection.commit()
except Exception as main_error:
    print(f"Une erreur s'est produite : {main_error}")
finally:
    cursor.close()
    connection.close()
