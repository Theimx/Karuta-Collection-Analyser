import csv

fileToAnalyse = r"Theimx.csv"

frames = []
wl = 0
total_value = 0
burnValue = 0
value = 0
top_cards = []
sp = []
bulk = 0

def determine_print_type(print_number):
    if 1 <= print_number <= 10:
        return "Special Print"
    elif 11 <= print_number <= 100:
        return "Light Print"
    elif 101 <= print_number <= 1000:
        return "Mid Print"
    else:
        return "High Print"

def estimate_ticket_value(edition, print_type, wl):
    min_value = max_value = 0
    
    if edition == 1:
        if print_type == "Special Print":
            min_value, max_value = 2, 4
        elif print_type == "Light Print":
            min_value, max_value = 8, 14
        elif print_type == "Mid Print":
            min_value, max_value = 70, 100
        elif print_type == "High Print":
            min_value, max_value = 750, 950
    elif edition == 2:
        if print_type == "Special Print":
            min_value, max_value = 2, 4
        elif print_type == "Light Print":
            min_value, max_value = 8.2, 15.2
        elif print_type == "Mid Print":
            min_value, max_value = 65, 95
        elif print_type == "High Print":
            min_value, max_value = 720, 840
    elif edition == 3:
        if print_type == "Special Print":
            min_value, max_value = 2, 4
        elif print_type == "Light Print":
            min_value, max_value = 8, 15
        elif print_type == "Mid Print":
            min_value, max_value = 60, 90
        elif print_type == "High Print":
            min_value, max_value = 590, 700
    elif edition == 4:
        if print_type == "Special Print":
            min_value, max_value = 2, 4
        elif print_type == "Light Print":
            min_value, max_value = 7, 13
        elif print_type == "Mid Print":
            min_value, max_value = 55, 85
        elif print_type == "High Print":
            min_value, max_value = 380, 470
    elif edition == 5:
        if print_type == "Special Print":
            min_value, max_value = 2, 4
        elif print_type == "Light Print":
            min_value, max_value = 8.1, 12.1
        elif print_type == "Mid Print":
            min_value, max_value = 65, 80
        elif print_type == "High Print":
            min_value, max_value = 200, 240
    elif edition == 6:
        if print_type == "Special Print":
            min_value, max_value = 2, 4
        elif print_type == "Light Print":
            min_value, max_value = 8, 11
        elif print_type == "Mid Print":
            min_value, max_value = 55, 70
        elif print_type == "High Print":
            min_value, max_value = 190, 220
    elif edition == 7:
        if print_type == "Special Print":
            min_value, max_value = 2, 4
        elif print_type == "Light Print":
            min_value, max_value = 9, 12
        elif print_type == "Mid Print":
            min_value, max_value = 50, 65
        elif print_type == "High Print":
            min_value, max_value = 140, 180
    
    if min_value == 0 and max_value == 0:
        return 0  
    
    avg_value = (min_value + max_value) / 2  # Moyenne des valeurs
    return wl / avg_value  


frame_values = {  
    'yearoftherat': 3,     'yearoftherabbit': 3, 'yearofthesheep': 3, 'yearofthedragon': 3,
    'yearoftheboar': 3,    'yearoftheox': 3,     'yearofthehorse': 3, 'yearofthedog': 3,
    'yearoftherooster': 3, 'yearofthesnake': 3,  'yearofthetiger': 3, 'yearofthemonkey':3,

    'mingvase': 5, 'springrain': 4, 'alienalloy': 7, 'kitsune': 12,

    'cherryberry': 3, 'carnations': 3, 'blossom': 3, 'musicalnotes': 3,
    'abandonedchurch': 3, 'labpunk': 3,

    'grimrose': 30, 'apollo': 30, 'ripple': 20, 'roseknight': 49,

    'archlight': 0, 'ashes': 0, 'ascendant': 0, 'autumnbreeze': 0, 'autumnview': 0,
    'azureclaw': 0, 'barbecue': 0, 'baroque': 0, 'beach': 0, 'beachtowel': 0,
    'bloodmoonbite': 0, 'boneslasher': 0, 'brass': 0, 'bridesmaid': 0, 'brokenmirror': 0,
    'bubbletea': 0, 'bunnypaws': 0, 'butterflywoods': 0, 'butterflygarden': 0,
    'chaosborn': 0, 'cleave': 0, 'coffeeshop': 0, 'coralreef': 0, 'cosmicentity': 0,
    'crystalwings': 0, 'crystallinelocket': 0, 'crow': 0, 'cursedplace': 0, 'divinity': 0,
    'dragonfruit': 0, 'dragonhunt': 0, 'easel': 0, 'edofurin': 0, 'electrified': 0,
    'explosion': 0, 'faerieforest': 0, 'flyingdragon': 0, 'frenchmaid': 0,
    'gamingchair': 0, 'gildedstars': 0, 'glinted': 0, 'glory': 0, 'goldrank': 0,
    'gothiccloak': 0, 'gothictower': 0, 'groomsman': 0, 'hacker': 0, 'hangingscrolls': 0,
    'harpstring': 0, 'heartbreak': 0, 'heartofsilver': 0, 'higasa': 0, 'holyknight': 0,
    'husband': 0, 'icicle': 0, 'illusion': 0, 'infinityvoid': 0, 'interface': 0,
    'islandluau': 0, 'japanesealley': 0, 'karutaboy': 0, 'kawaiibento': 0,
    'lifedeath': 0, 'lich': 0, 'lighthousestorm': 0, 'livestream': 0, 'magicalgirl': 0,
    'magitek': 0, 'magitor': 0, 'magus': 0, 'malicetree': 0, 'mahou': 0,
    'manekineko': 0, 'mermaid': 0, 'midnightbloom': 0, 'mirroredenergy': 0, 'nether': 0,
    'nightfestival': 0,

    'nightmare': 25, 'nightooze': 3, 'nova': 40, 'nightwalker': 20, 'wizardshut': 3,
    'winnerspodium': 3
}

with open(fileToAnalyse, 'r', newline='', encoding='utf-8') as fichier:
    reader = csv.reader(fichier)  

    next(reader)# Ignore la première ligne (en-tête)

    for ligne in reader:
        burnValue += int(ligne[8])  
        wl += int(ligne[16])

        if ligne[11]:  # Vérifie si la colonne 12 (index 11) n'est pas vide
            frames.append(ligne[11])

        edition = int(ligne[2])  
        print_number = int(ligne[1])  
        print_type = determine_print_type(print_number)  
        whishList = int(ligne[16])  
        ticket_value = (estimate_ticket_value(edition, print_type, whishList)* 100000000000)
        value += ticket_value

        card_name = ligne[0]  
        card_series = ligne[3]  
        card_code = ligne[4]  
        top_cards.append((card_name, card_series, card_code, ticket_value))
        if int(ligne[1]) <= 10:
            sp.append("Code : " + str(ligne[0]) + " Print : "+ str(ligne[1])+" Edition : "+str(ligne[2])+" : "+str(ligne[3])+ " " +str(ligne[4]))

        #Pour afficher toutes les cartes aillant une valeur supérieur a 1 ticket
        # if ticket_value >= (100000000000) and ligne[14] == "":
        #     print(ligne[3],ligne[4] ,ligne[0], round((ticket_value/100000000000),3), " Tickets" )

        #Pour afficher toutes les cartes aillant une valeur inferieurs a 0.3 tickets, affiche la somme
        # if ticket_value <= (100000000000/10) and ligne[14] == "":
        #     print(ligne[3] ,ligne[4] ,ligne[0], round((ticket_value/100000000000),3), " Tickets" )
        #     test += ticket_value

for frame in frames:
    if frame in frame_values:  
        total_value += frame_values[frame]

top_cards_sorted = sorted(top_cards, key=lambda x: x[3], reverse=True)[:20]

print(bulk/100000000000)
print(" ")
print("---------------------------------------------------------------------------------")
print(" ")
print(fileToAnalyse)
print(" ")
print("----- Statistiques --------------------------------------------------------------")
print(burnValue," Gold (Total Gold, Total Burn Value of the Collection )")
print(wl," Whishlist (Total Whishlist )")
print(" ")
print("----- Tickets -------------------------------------------------------------------")
print(total_value, " Tickets ( Values of the Frames applied in the collection )")
print(burnValue // 2500, "Tickets (In gold, Total burn value in tickets)")
print(round((value/100000000000)), "Tickets : Value of every card of the collection (Based on Print,Edition and Whishlist)")
print(" ")
print((total_value+ round((value/100000000000))),"  Tickets (Card + Frame Value)")
print(" ")

print("----- Top 20 Most Valuable Cards (Without frames ) -------------------------------")
print(" ")
for i, (name, series, code, val) in enumerate(top_cards_sorted, 1):
    print(f"- {name}, {series}, {code}, {round(val/100000000000)} Tickets")
print(" ")
print("---------------------------------------------------------------------------------")
print("All the frames'values are not in the software yet so your collection can be worth more than the price tell here.")
print("Frames : ",frames)
print(" ")
print("Special Print : ")
for i in sp :
    print(i)
