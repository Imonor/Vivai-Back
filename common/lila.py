"""File for Machine Learning Services"""

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
        return f'Très peu d\'eau nécéssaire. Votre {species} semble être une descandant du cactus !'
    else:
        return f'Votre {species} a soif ! On dirait Ilan au bar le vendredi soir...'

def temperature(species):
    cold = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["coldResistance"], "species", "=", species)
    if cold == "Fragile":
        return f'Votre {species} est très fragile et supporte mal le froid. Placez là dans un environnement assez chaud. ' + soleil(species)
    elif cold == "Moyenne":
        return f'Votre {species} supporte assez bien le froid, vous pouvez la placez dans une pièce à température ambiante \
            et la sortir par beau temps. ' + soleil(species)
    else:
        return f'Votre {species} supporte toutes les températures ! Rien ne lui fait peur ! ' + soleil(species)

def entretien(species):
    ent = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["careLevel"], "species", "=", species)
    if ent == "Facile":
        return f'Ne vous inquiétez pas, votre {species} n\a pas énormément besoin de vous. Vérifier son état une fois par semaine devrait suffir.'
    elif ent == "Modéré":
        return f'Votre {species} a besoin d\'un peut d\'attention de votre part ! Pensez à vous occuper d\'elle 2 à 3 fois par semaine.'
    else:
        return f'Vous feriez mieux de vous occuper de votre {species} comme d\'un bébé ! Pensez à vérifiez son état tous les jours.'
        
def hauteur(species):
    height = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["heightMature"], "species", "=", species)["heightMature"]["S"]
    return f'Votre {species} peut atteindre une hauteur de {height} à maturité !'

def cadeaux(species):
    return f' Cette idée est une très bonne idée ! Votre {species} fera forcément plaisir !'


switcher = {
    "arrosage": arrosage,
    "soleil": soleil,
    # 2: tailler, 
    "temperature": temperature, 
    # 4: utilisation, 
    "entretien": entretien, 
    "cadeaux": cadeaux, 
    # 7: varietes, 
    # 8: planter, 
    # 9: maladies, 
    "hauteur": hauteur
}

def get_lila_response(event, context):
    try:
        parameters = utilities.get_parameters(event, [PARAM_LILA_REQUEST, PARAM_USER_ID], [])
        # lila_request = parameters[PARAM_LILA_REQUEST]
        user_id = parameters[PARAM_USER_ID]
        lila_request = parameters[PARAM_LILA_REQUEST]

        # Appel de l'API ML avec retour de l'intention, du score, de l'espèce.
        parameters = {"q" : lila_request}
        response = requests.get("http://todoo.xyz:5000/", params = parameters).json()[0]

        intention = response["results"][0]
        score = response["results"][1]
        species = response["plant"]

        # Score inférieur à 50%
        if score < 0.5:
            return utilities.generate_http_response({"Reponse": "Je n'ai pas compris ta question. Articule s'il te plaît."}), 200

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
