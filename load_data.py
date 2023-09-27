import psycopg2

# Informations de connexion à la base de données PostgreSQL
db_host = "localhost"
db_port = "5432"
db_name = "mtg"
db_user = "g_jolly"
db_password = "Production202306!"

# Chemin vers le fichier PSQL contenant les commandes spécifiques à PostgreSQL
psql_file_path = "C:/Users/guill/OneDrive/Documents/Boulot/projet_mtg/Input/AllPrintings.psql"

# Chemin vers le fichier de rejet
rejection_file_path = "C:/Users/guill/OneDrive/Documents/Boulot/projet_mtg/Rejection.sql"

try:
    # Établir une connexion à la base de données
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )

    # Créer un curseur pour exécuter les commandes SQL
    cursor = conn.cursor()

    # Lire le fichier PSQL
    with open(psql_file_path, 'r', encoding='utf-8') as psql_file:
        psql_commands = psql_file.read()

    # Remplacer les caractères de nouvelle ligne par des espaces
    psql_commands = psql_commands.replace('\n', ' ')

    # Diviser les commandes PSQL en instructions individuelles
    commands = psql_commands.split(';')

    # Ouvrir le fichier de rejet en mode écriture
    with open(rejection_file_path, 'w', encoding='utf-8') as rejection_file:
        for command in commands:
            trimmed_command = command.strip()
            if trimmed_command:  # Vérifier si la commande n'est pas vide
                try:
                    cursor.execute(trimmed_command)
                    #print("Commande exécutée avec succès.")
                except Exception as e:
                    #print(f"Erreur lors de l'exécution de la commande : {str(e)}")
                    # Écrire la commande rejetée dans le fichier de rejet
                    rejection_file.write(trimmed_command + ";\n")

    # Valider les modifications et fermer la connexion
    conn.commit()
    cursor.close()
    conn.close()

    print("Toutes les commandes ont été exécutées avec succès.")
except Exception as e:
    print(f"Erreur lors de l'exécution des commandes : {str(e)}")
