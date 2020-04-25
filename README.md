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
| getSupportedPlants | GET  | Returns the list of supported plants matching the search, if given, else returns all supported plants | app/getSupportedPlants | search: the searched plant (**OPTIONNAL**) | [{"species": "Basilic", "websiteUrl": "http://basilic.fr"}, {...}] |
| insertPlant       | PUT  | Insert a plant for the user | app/insertPlant | userId(string), species(string) (**REQUIRED**), location(string), temperature(string), sunExpo(string), shared(boolean) (**OPTIONAL**)  | {"userPlantId" : 29, "userId": "axY-90eju-&mp", "plantId" : 19} |
| getListPlants    | GET   | Returns the list of plants for the user   | app/getListPlants | userId : id of the user (**REQUIRED**)  | [{"id": 10, "plantId": 1, "userId": "10", "location": "Salon", "temperature": 20.0, "sunExpo": "1", "shared": true}, {"id": 18, "plantId": 2, "userId": "10", "location": "Cuisine", "temperature": 22.2, "sunExpo": "NULL", "shared": false},  {"id": 21, "plantId": 3, "userId": "10", "location": "NULL", "temperature": "NULL", "sunExpo": "NULL", "shared": false}] |
