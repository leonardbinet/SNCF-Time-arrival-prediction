"""
This module compute API requests.
"""

import os
import json
import requests
import pandas as pd
from configuration import USER, PASSWORD

# Parameters


def compute_api_request(path):
    base = "https://api.sncf.com/v1/"
    payload = {
        "start_page": 0,
        "count": 100,
    }
    url = os.path.join(base, path)
    r = requests.get(url=url, auth=(USER, PASSWORD), params=payload)
    if r.status_code == 200:
        parsed = json.loads(r.text)

        # init
        try:
            df_pagination = pd.DataFrame(
                parsed["pagination"],
                index=range(0, len(parsed["pagination"])))
            print("Correctly imported pagination")
        except KeyError:
            print("No pagination")
            df_pagination = "nope_pagination"

        try:
            df_links = pd.DataFrame(parsed["links"])
            print("Correctly imported links")
        except KeyError:
            print("No links")
            df_links = "nope_link"

        try:
            last_el = url.rsplit('/', 1)[-1]
            df_items = pd.DataFrame(parsed[last_el])
            print("Correctly imported " + last_el)
        except KeyError:
            print("No " + url.rsplit('/', 1)[-1])
            df_items = "nope_item"
        return df_pagination, df_links, df_items

df1, df2, df3 = compute_api_request("coverage/sncf/lines")
print(df1)
print(df2)
print(df3)
