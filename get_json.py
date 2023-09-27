import os
import requests
import json
import logging

# Configurez la journalisation pour afficher les messages de niveau INFO dans la console
logging.basicConfig(level=logging.INFO)

# Fonction pour récupérer le JSON depuis MTGJSON et l'enregistrer dans un fichier
def fetch_mtgjson_data_and_save_to_file(output_directory):
    try:
        # Vérifier si le répertoire de sortie existe, sinon le créer
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        url = 'https://mtgjson.com/api/v5/AllPrintings.json'
        logging.info("Tentative de récupération du JSON depuis MTGJSON...")
        response = requests.get(url)

        if response.status_code == 200:
            mtg_data = response.json()

            # Chemin complet du fichier de sortie
            output_file_path = os.path.join(output_directory, 'AllPrintings.json')

            # Enregistrer les données JSON dans le fichier
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(mtg_data, output_file, ensure_ascii=False, indent=4)

            logging.info(f"Les données ont été enregistrées avec succès dans {output_file_path}.")
        else:
            logging.error('La requête a échoué avec le code', response.status_code)
    except Exception as error:
        logging.error("Une erreur s'est produite :", error)

if __name__ == "__main__":
    output_directory = os.path.join(os.getcwd(), 'input')  # Répertoire de sortie
    fetch_mtgjson_data_and_save_to_file(output_directory)
