# SNCF ARRIVAL TIME PREDICTION


## GOAL
The goal of this project is to predict in real-time the arrival time of trains given some information about the network events.


## DATA SOURCES
Mostly SNCF API.

## USAGE
You first have to ask SNCF for an API key, and store it at the root of the repository within a secret.json file, like this:
```
 {
     "USER": "your_api_user"
 }
```
This is made to not save one's API key on github (in .gitignore).

Then to launch functions, you have to call them from the main function.
This architecture is easier because of python import system.

### Extract data from API:
You can simply launch the main module, and it will get data from the api (5 pages max per item), and save csv files in a Data folder.
## TREE VIEW
```
├── API
│   ├── Documentation.md
│   ├── Queries_shortcuts.md
│   ├── __init__.py
│   ├── api_request.py
│   └── utils.py
├── README.md
├── configuration.py
├── main.py
├── secret.json
```
## ROADMAP
Explain data.
