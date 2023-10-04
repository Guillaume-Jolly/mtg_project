
input_files='C:/Users/GuillaumeJOLLY/Documents/mtg_projet/Output/AllPricesToday_aplati.json'
output_files='C:/Users/GuillaumeJOLLY/Documents/mtg_projet/Output/AllPricesToday_aplati.csv'

with open(input_files, 'r') as source_file:
    # Ouvrir le fichier de destination en mode écriture
    with open(output_files, 'w') as destination_file:
        ligne_compteur = 0
        for ligne in source_file:            
            # Incrémenter le compteur de lignes
            ligne_compteur += 1
            
            # Commencer à partir de la troisième ligne
            if ligne_compteur > 3 and ligne[:2]=='  ':
                parts = ligne.split("_")
                # Extraire les éléments nécessaires
                uuid = parts[1]
                platform = parts[2]
                retail = parts[3]
                if parts[4][0:8] == 'currency' :
                    state = ''
                    foil = ''
                    date = ''
                    price = ''
                    # Diviser la partie contenant la date en utilisant ":"
                    currency = parts[4].split(":")[1].strip().replace('"','').replace(',','')
                else :
                    state = parts[4]
                    foil = parts[5]
                    # Diviser la partie contenant la date en utilisant ":"
                    date_and_price = parts[6].split(":")
                    date = date_and_price[0][:-1]
                    price = date_and_price[1].strip().replace(',','')
                    currency=''
                destination_file.write(f"{uuid};{platform};{retail};{state};{foil};{date};{price};{currency}" + '\n')


#f182e364-0439-5594-a6e6-75f7889ccf45;mtgo;cardhoarder;retail;normal;2023-09-26;0.05