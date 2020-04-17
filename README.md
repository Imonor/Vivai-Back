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

