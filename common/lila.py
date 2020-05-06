"""File for Machine Learning Services"""

import random
from botocore.exceptions import ClientError

import requests
import common.utilities as utilities
import common.db_dealer as db_dealer

PARAM_LILA_REQUEST = "lilaRequest"
PARAM_USER_ID = "userId"

def soleil(species): 
    sun = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["sunNeed"], "species", "=", species)
    if sun == "Soleil": 
        return f'Votre {species} à besoin de {sun}.'
    elif sun == "Ombre":
        return f'Il est conseillé de mettre votre {species} à l\'{sun}. Il ne faudrait pas faire une insolation...'
    else:
        return f'Votre {species} préfère vivre dans un environnement ombragé.'

def arrosage(species):
    arr = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["waterNeed"], "species", "=", species)
    if arr == "Moyen":
        return f'Votre {species} a besoin d\'une quantité d\'eau normale. Arrosez 2 à 3 fois par semaine.'
    elif arr == "Faible":
        return f'Très peu d\'eau nécéssaire. Votre {species} semble être un·e descendant·e du cactus !'
    else:
        return f'Si votre {species} est à l\'intérieur, vous pouvez l\'arroser plusieurs fois par semaine. \
            En extérieur, vous devez lui apporter de l\'eau abondamment et régulièrement.'

def temperature(species):
    cold = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["coldResistance"], "species", "=", species)
    if cold == "Fragile":
        return f'Votre {species} est très fragile et supporte mal le froid. Placez votre plante dans un environnement assez chaud. ' + soleil(species)
    elif cold == "Moyenne":
        return f'Votre {species} supporte assez bien le froid, vous pouvez placer votre plante dans une pièce à température ambiante \
            et la sortir par beau temps. ' + soleil(species)
    else:
        return f'Votre {species} résiste au gel ! Rien ne lui fait peur ! ' + soleil(species)

def entretien(species):
    ent = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["careLevel"], "species", "=", species)
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
    return db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["pest"], "species", "=", species)

def planter(species):
    plantation_months = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["plantationMonths"], "species", "=", species)
    where_to_plant = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["whereToPlant"], "species", "=", species)
    return f'{where_to_plant} Pour une meilleure pousse, il est préférable de planter votre {species} de \
        {plantation_months[0]} à {plantation_months[len(plantation_months) - 1]}'

def anecdote(species):
    ecological_tips = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["ecologicalTips"], "species", "=", species)
    history = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["history"], "species", "=", species)
    if not ecological_tips and not history:
        return f'Je n\'ai aucune anecdote à raconter sur votre {species}...'
    else:
        return f'Mmh oui j\'ai quelques anecdotes en stock pour votre {species} ! \
            {random.choice(ecological_tips)} {random.choice(history)}' 

switcher = {
    "arrosage": arrosage,
    "soleil": soleil,
    # 2: tailler, 
    "temperature": temperature, 
    # 4: utilisation, 
    "entretien": entretien, 
    "cadeaux": cadeaux, 
    # 7: varietes, 
    "planter": planter, 
    "maladies": maladies, 
    "hauteur": hauteur,
    "anecdote": anecdote
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

        # Score inférieur à 50%
        if score < 0.7:
            return utilities.generate_http_response({"Response": "Je n'ai pas compris ta question. Articule s'il te plaît."}), 200

        # Si l'espèce est nulle
        if species is None:
            try :
                species = db_dealer.get_attributes(db_dealer.USER_PLANT_TABLE, ["species"], "userId", "=", user_id)["species"]["S"]
            except ClientError as error:
                raise error

        try:
            response = switcher[intention](species)
        except ClientError as error:
            raise error

        return utilities.generate_http_response({"Response": response}), 200

    except (ClientError, utilities.MissingParameterException) as error:
        return utilities.handle_error(error)
