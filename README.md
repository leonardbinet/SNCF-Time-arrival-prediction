# SNCF ARRIVAL TIME PREDICTION


## GOAL
The goal of this project is to predict in real-time the arrival time of trains given some information about the network events.


## DATA SOURCES
Mostly SNCF API.

## USAGE
To use api_request.py, you first have to ask SNCF for an API key, and store it at the root of the repository within a secret.json file, like this:
```
 {
     "USER": "your_api_user"
 }
```
This is made to not save one's API key on github (in .gitignore).
```
├── API
│   ├── Documentation.md
│   └── Queries_shortcuts.md
├── README.md
├── api_request.py
├── configuration.py
└── secret.json
```
## ROADMAP


https://data.sncf.com/api/fr/documentation
