"""File for Machine Learning Services"""

import random
from botocore.exceptions import ClientError

import requests
import common.utilities as utilities
import common.db_dealer as db_dealer

PARAM_LILA_REQUEST = "lilaRequest"
PARAM_USER_ID = "userId"

def soleil(species): 
    sun = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["sunNeed"], "species", "=", species)["sunNeed"]["S"]
    if sun == "Soleil": 
        return f'Votre {species} doit avoir du soleil direct toute la journée. En intérieur, c’est directement (moins d’1 m) devant une fenêtre orientée sud ou ouest.'
    elif sun == "Ombre":
        return f'Votre {species} doit être à l\'ombre d\'autres plantes. En intérieur, c’est le cas des pièces en hiver, des fenêtres au nord ou en partie occultées et quand la plante est loin de la fenêtre (+ de 2 m).'
    else:
        return f'Votre {species}  doit avoir du soleil une partie de la journée seulement. En intérieur, c’est devant une fenêtre à l’est ou plus éloignée d’une fenêtre orientée sud ou ouest.'

def arrosage(species):
    arr = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["waterNeed"], "species", "=", species)["waterNeed"]["S"]
    if arr == "Moyen":
        return f'Votre {species} a besoin d\'une quantité d\'eau normale. Arrosez 2 à 3 fois par semaine.'
    elif arr == "Faible":
        return f'Très peu d\'eau nécéssaire. Pour une plante d\'intérieur, arroser tous les mois. Pour une plante d\'extérieur, elle supporte bien la sécheresse.'
    else:
        return f'Si votre {species} est à l\'intérieur, vous pouvez l\'arroser plusieurs fois par semaine. \
            En extérieur, vous devez lui apporter de l\'eau abondamment et régulièrement.'

def temperature(species):
    cold = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["coldResistance"], "species", "=", species)["coldResistance"]["S"]
    if cold == "Fragile":
        return f'Votre {species} est très fragile et supporte mal le froid. Placez votre plante dans un environnement assez chaud. ' + soleil(species)
    elif cold == "Moyenne":
        return f'Votre {species} supporte assez bien le froid, vous pouvez placer votre plante dans une pièce à température ambiante \
            et la sortir par beau temps. ' + soleil(species)
    else:
        return f'Votre {species} résiste au gel ! Rien ne lui fait peur ! ' + soleil(species)

def entretien(species):
    ent = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["careLevel"], "species", "=", species)["careLevel"]["S"]
    if ent == "Facile":
        return f'Ne vous inquiétez pas, votre {species} n\'a pas énormément besoin de vous. Vérifier son état une fois par semaine devrait suffire.'
    elif ent == "Modéré":
        return f'Votre {species} a besoin d\'un peu d\'attention de votre part ! Pensez à vous en occuper 2 à 3 fois par semaine.'
    else:
        return f'Vous feriez mieux de vous occuper de votre {species} comme d\'un bébé ! Pensez à vérifiez son état tous les jours.'

def hauteur(species):
    height = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["height"], "species", "=", species)["height"]["S"]
    return f'Votre {species} peut atteindre une hauteur de {height} à maturité !'

def cadeaux(species):
    return f'Cette idée est une très bonne idée ! Votre {species} fera forcément plaisir !'

def maladies(species):
    plant = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["pest"], "species", "=", species)
    if "pest" in plant:
        return plant["pest"]["S"]

    return ""

def planter(species):
    plant = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["plantationMonths", "soilType"], "species", "=", species)
    response = ""
    if "soilType" in plant:
        response = plant["soilType"]["S"]

    response += f' Pour une meilleure pousse, il est préférable de planter votre {species} de \
        {plant["plantationMonths"]["SS"][0]} à {plant["plantationMonths"]["SS"][-1]}'
    return response

def anecdote(species):
    plant = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["ecologicalTips", "history"], "species", "=", species)
    if not plant:
        return f'Je n\'ai aucune anecdote à raconter sur votre {species}...'

    item_history = plant.get("history", None)
    item_tips = plant.get("ecologicalTips", None)

    history = item_history["S"] if item_history else "NULL"
    tips = item_tips["S"] if item_tips else "NULL"

    if history == "NULL" and tips == "NULL":
        return f'Je n\'ai aucune anecdote à raconter sur votre {species}...'

    response = f'Mmh oui j\'ai quelques anecdotes en stock pour votre {species} !\n'

    if tips != "NULL":
        response += plant["ecologicalTips"]["S"]

    else:
        response += plant["history"]["S"]

    return response

def varietes(species):
    return ("Je n'ai pas compris votre question...")

def tailler(species):
    return ("Je n'ai pas compris votre question...")

def utilisation(species):
    return ("Je n'ai pas compris votre question...")

SWITCHER = {
    "arrosage": arrosage,
    "soleil": soleil,
    "tailler": tailler, 
    "temperature": temperature, 
    "utilisation": utilisation, 
    "entretien": entretien, 
    "cadeaux": cadeaux, 
    "varietes": varietes,
    "planter": planter,
    "maladies": maladies, 
    "hauteur": hauteur,
    "anecdotes": anecdote
}

def get_lila_response(event, context):
    try:
        parameters = utilities.get_parameters(event, [PARAM_LILA_REQUEST, PARAM_USER_ID], [])
        user_id = parameters[PARAM_USER_ID]
        lila_request = parameters[PARAM_LILA_REQUEST]

        # Appel de l'API ML avec retour de l'intention, du score, de l'espèce.
        parameters = {"q" : lila_request}
        response = requests.get("http://todoo.xyz:5000/", params = parameters).json()[0]

        intention = response["results"][0]
        score = response["results"][1]
        species = response["plant"]

        # Score inférieur à 10%
        if score < 0.1:
            return utilities.generate_http_response({"Response": "Je n'ai pas compris votre question... Pourriez-vous reformuler ?"}), 200

        # Si l'espèce est nulle
        if species is None:
            return utilities.generate_http_response({"Response": "De quelle espèce parlez-vous ?"}), 200

        try:
            response = SWITCHER[intention](species)
        except ClientError as error:
            raise error

        return utilities.generate_http_response({"Response": response}), 200

    except (ClientError, utilities.MissingParameterException) as error:
        return utilities.handle_error(error)
