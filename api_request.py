"""
This module compute API requests.
"""

import configuration
import requests
import json


# parameters
url = "https://api.sncf.com/v1/"

r = requests.get(url)
