"""
This module compute API requests.
"""

import os
import json
import requests
import pandas as pd


def compute_api_request(path, api_user):
    print("LAUNCH REQUEST ON SNCF API FOR " + path)
    page = 0
    # init

    def get_page(page):
        print("Import on page " + str(page))
        base = "https://api.sncf.com/v1/"
        payload = {
            "start_page": page,
            "count": 100,
        }
        url = os.path.join(base, path)
        r = requests.get(url=url, auth=(api_user, ""), params=payload)
        if r.status_code == 200:
            parsed = json.loads(r.text)

        try:
            pagination = parsed["pagination"]
            print("Correctly imported pagination")
        except KeyError:
            print("No pagination")
            pagination = "nope_pagination"
        try:
            df_disruptions = pd.DataFrame(parsed["disruptions"])
            print("Correctly imported disruptions")
        except KeyError:
            print("No disruptions")
            df_disruptions = "nope_disruptions"
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
        result = {
            'keys': parsed.keys(),
            'pagination': pagination,
            'links': df_links,
            'items': df_items,
            'disruptions': df_disruptions,
        }
        return result

    # compute first with 100 lines
    first = get_page(0)

    # initialize result dictionary
    # one dataframe
    final_result = {
        "links": first["links"],
        "pagination": pd.DataFrame(first["pagination"], index=[0]),
        "items": first["items"],
        "disruptions": first["disruptions"],
        "keys": first["keys"],  # list all keys present in first page
    }
    # find number of requests to make
    hundreds = first["pagination"][
        "total_result"] // first["pagination"]["items_per_page"]

    # compute necessary queries
    for page in range(1, hundreds + 1):
        page_result = get_page(page)

        # append results
        final_result["items"] = pd.concat(
            [final_result["items"], page_result["items"]], ignore_index=True)
        final_result["disruptions"] = pd.concat(
            [final_result["disruptions"], page_result["disruptions"]], ignore_index=True)
        page_pagination = pd.DataFrame(page_result["pagination"], index=[page])
        final_result["pagination"] = pd.concat(
            [final_result["pagination"], page_pagination]
        )

    # print results shape
    print("Imported pagination shape: \n", final_result["pagination"].shape)
    print("Imported links shape: \n", final_result["links"].shape)
    print("Imported disruptions shape: \n", final_result["disruptions"].shape)
    print("Imported items shape: \n", final_result["items"].shape)
    print("Keys present in first page: ", final_result["keys"])

    return final_result
