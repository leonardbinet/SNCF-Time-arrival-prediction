"""
This module computes API requests.
"""

import os
import json
import requests
import pandas as pd


def compute_api_request(path, api_user, page_limit=10, debug=False):
    print("LAUNCH REQUEST ON SNCF API FOR " +
          path + " WITH LIMIT " + str(page_limit))

    def get_page(page, count):
        print("Import on page " + str(page))
        base = "https://api.sncf.com/v1/"
        payload = {
            "start_page": page,
            "count": count,
        }
        url = os.path.join(base, path)
        r = requests.get(url=url, auth=(api_user, ""), params=payload)
        if r.status_code == 200:
            parsed = json.loads(r.text)
        else:
            print("Request failed " + str(r.status_code))
            result = {
                "request": r,
                "scrap": False,
                "items": pd.DataFrame()
            }
            return result

        try:
            pagination = parsed["pagination"]
            if debug:
                print("Correctly imported pagination")
        except KeyError:
            print("No pagination")
            pagination = "nope_pagination"
        try:
            df_disruptions = pd.DataFrame(parsed["disruptions"])
            if debug:
                print("Correctly imported disruptions")
        except KeyError:
            print("No disruptions")
            df_disruptions = "nope_disruptions"
        try:
            df_links = pd.DataFrame(parsed["links"])
            if debug:
                print("Correctly imported links")
        except KeyError:
            print("No links")
            df_links = "nope_link"

        try:
            last_el = url.rsplit('/', 1)[-1]
            df_items = pd.DataFrame(parsed[last_el])
            if debug:
                print("Correctly imported " + last_el)
        except KeyError:
            print("No " + url.rsplit('/', 1)[-1])
            df_items = "nope_item"
        result = {
            'keys': list(parsed.keys()),
            'pagination': pagination,
            'links': df_links,
            'items': df_items,
            'disruptions': df_disruptions,
            'scrap': True
        }
        return result

    # compute first with 100 lines
    nbr_per_page = 100
    first = get_page(0, nbr_per_page)
    if not first["scrap"]:
        print("Scrap failed.")
        return first
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
    nbr_elements = first["pagination"][
        "total_result"]
    hundreds = nbr_elements // nbr_per_page

    page_limit = min(page_limit, hundreds + 1)
    print("-" * 50)
    print("There are " + str(nbr_elements) + " elements with " +
          str(nbr_per_page) + " elements per page. Limit is " + str(page_limit) + ".")
    print("-" * 50)
    # compute necessary queries
    for page in range(1, page_limit):
        page_result = get_page(page, nbr_per_page)

        # append results
        final_result["items"] = pd.concat(
            [final_result["items"], page_result["items"]], ignore_index=True)
        final_result["disruptions"] = pd.concat(
            [final_result["disruptions"], page_result["disruptions"]], ignore_index=True)
        page_pagination = pd.DataFrame(page_result["pagination"], index=[page])
        final_result["pagination"] = pd.concat(
            [final_result["pagination"], page_pagination]
        )

    # print results
    print("-" * 50)
    print("RESULTS")
    print("Imported pagination shape: \n", final_result["pagination"].shape)
    print("Imported links shape: \n", final_result["links"].shape)
    print("Imported disruptions shape: \n", final_result["disruptions"].shape)
    print("Imported items shape: \n", final_result["items"].shape)
    print("Keys present in first page: ", final_result["keys"])
    print("-" * 50)

    return final_result
