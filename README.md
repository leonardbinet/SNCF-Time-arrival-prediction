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
```
├── API
│   ├── Documentation.md
│   ├── Queries_shortcuts.md
│   ├── __init__.py
│   └── api_request.py
├── README.md
├── __init__.py
├── configuration.py
├── main.py
└── secret.json
```

Then to launch functions, you have to call them from the main function.

This architecture is easier because of python import system.

## ROADMAP


https://data.sncf.com/api/fr/documentation
