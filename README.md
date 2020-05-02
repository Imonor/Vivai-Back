# Vivai-Back - ReadMe

## API endpoints
The name field is the name of the function as it is described in the serverless.yml file and the add.py file. It has nothing to do with the associated endpoint URL.
There is a separation between services that need a user to be connected and those that do not need this :
    - 'https://BASEURL/api/SERVICE' for the non protected ones
    - 'https://BASEURL/authorized/SERVICE' for the protected ones
Example: to invoke the function named hello: `GET https://BASEURL/app/hello`


| Name              | Type | Description                            | URL             | Parameters         | Example response                                                                                                                      |
|-------------------|------|----------------------------------------|-----------------|--------------------|-------------------------------------------------------------------------------------------------------------------------------|
| hello             | GET  | Says hello                             | app/hello       | null               | {"message": "Hello world !"} |
| getSupportedPlants | GET  | Returns all supported plants | app/getSupportedPlants | null | [{"species": "Basilic", "websiteUrl": "http://basilic.fr"}, {...}] |
| insertUserPlant       | PUT  | Insert a plant for the user | app/insertUserPlant | userId(string), species(string) (**REQUIRED**), nickname(string), location(string), temperature(string), sunExpo(string), shared(boolean) (**OPTIONAL**)  | {"userPlantId" : "9acb5af3-40c3-485d-b6a0-d2f48a5dac80", "plantId" : "219bd212-2b5a-495f-b090-3fe4ad69c952"} |
| getListPlants    | GET   | Returns the list of plants for the user   | app/getListPlants | userId : id of the user (**REQUIRED**)  | [{"id": "d71cda2b-b329-4fcd-9daa-e1fe5be374cc", "plantId": "9acb5af3-40c3-485d-b6a0-d2f48a5dac80", "userId": "9acb5af3-40c3-485d-b6a0-d2f48a5dac80", "nickname": "NULL", "location": "NULL", "temperature": "NULL", "sunExpo": "NULL", "shared": false, "picUrl": "http://basilic.png", "species": "Basilic"}, {...}] |
| deleteUserPlant | PUT | Delete the specified plant for a user | app/deleteUserPlant | userId(string), userPlantId(string) | {"Message": "Plant successfully deleted} |
| getPlantInfos | GET | Get infos for specified plant | app/getPlantInfos | plantId(string) | {"careLevel": "Modéré", "coldResistance": "Fragile", "family": "Lamiacées", "growth": "Normale", "heightMature": "0,15 à 1 m", "picUrl": "https://media.ooreka.fr/public/image/plant/16/mainImage-source-9167557.jpg","species": "Basilic", "sunNeed": "Soleil", "waterNeed": "Moyen", "widthMature": "0,7 à 1,2 m" } |
| getUserPlantInfos  | GET   | Returns the user plant | app/getUserPlantInfos | userId(string), userPlantId(string) (**REQUIRED**)  | {"id": "d71cda2b-b329-4fcd-9daa-e1fe5be374cc", "plantId": "9acb5af3-40c3-485d-b6a0-d2f48a5dac80", "userId": "9acb5af3-40c3-485d-b6a0-d2f48a5dac80", "nickname": "NULL", "location": "NULL", "temperature": "NULL", "sunExpo": "NULL", "shared": false, "picUrl": "http://basilic.png", "species": "Basilic"} |
| getRandomInfos | GET | Gives random infos and anecdotes on plants | app/getRandomInfos | | {"Info": "Le basilic vient du nom latin..."} |
| getSharedPlants | GET | Returns all shared plants of given plantID | app/getSharedPlants | plantId(string) | [{"id": "8943799a-9228-4fac-9b35-33409ad7cb2e", "plantId": "9acb5af3-40c3-485d-b6a0-d2f48a5dac80", "userId": "f734bc6d-b516-404a-8bdb-21a26f3a85fb", "nickname": "Henry", "location": "Jardin", "temperature": "17,5°C - 20°C","sunExpo": "2", "species": "Basilic"}] | 
