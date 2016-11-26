"""
This module computes API requests.
"""

import os
import json
import requests
import pandas as pd

from multiprocessing import Pool
from API.utils import flattenjson, flatten_columns, flatten_dataframe

# http://www.rueckstiess.net/research/snippets/show/ca1d7d90


def unwrap_self_f(arg, **kwarg):
    return ApiRequest.compute_request_page(*arg, **kwarg)


class ApiRequest:

    def __init__(self, user, path):
        self.core_path = "https://api.sncf.com/v1/"
        self.user = user
        self.path = os.path.join(self.core_path, path)
        # Here are stored all requests results
        self.results = {}
        self.parsed_results = {}
        self.first_request_status = False
        self.total_result = False
        print("Computing API request for " + self.path)

    def compute_request_page(self, page=0, debug=False, count=100):
        if debug:
            print("Import on page " + str(page))
        # Parameters of request
        payload = {
            "start_page": page,
            "count": count,
        }
        # Compute request
        request_result = requests.get(
            url=self.path, auth=(self.user, ""), params=payload)
        # Save result
        self.results[page] = request_result
        # Save result success, and number of results, for first page.
        if request_result.status_code == 200 and page == 0:
            self.first_request_status = True
            self.extract_nbr_results()

    def extract_nbr_results(self):
        if not self.first_request_status:
            print("Cannot extract, because no successful request.")
        # Parse first request answer.
        parsed = json.loads(self.results[0].text)
        # Extract pagination part.
        pagination = parsed["pagination"]
        # Extract total_result
        self.total_result = pagination["total_result"]

    def compute_request_pages(self, page_limit=10, debug=False, count=100):
        # Compute first with 100 lines
        self.compute_request_page(0, count)
        if not self.total_result and not self.first_request_status:
            print("Fail, cound not successfully compute first request.")
        # Find number of requests to make
        blocs = self.total_result // count
        page_limit = min(page_limit, blocs + 1)
        if debug:
            print("-" * 50)
            print("There are " + str(self.total_result) + " elements with " +
                  str(count) + " elements per page. Limit is " + str(page_limit) + ".")
            print("-" * 50)
        # Compute necessary queries
        # Here multiprocessing
        pages = range(1, page_limit)
        pool = Pool(processes=10)
        pool.map(unwrap_self_f, zip(
            [self] * len(pages), pages, [debug] * len(pages), [count] * len(pages)))

        # for page in range(1, page_limit):
        #    self.compute_request_page(page, debug=debug, count=count)

    def explain(self):
        print("Détail des résultats")
        # TODO


class RequestParser:

    def __init__(self, request_results, asked_path):
        self.asked_path = asked_path
        self.results = request_results
        self.item_name = os.path.basename(asked_path)
        self.parsed = {}  # dictionary of page : dictionary
        self.nested_items = None  # will be a dict
        self.unnested_items = None  # will be a dict
        self.links = []  # first page is enough
        self.disruptions = []  # append all
        self.keys = []  # collect keys found in request answer

    def set_results(self, request_results):
        self.results = request_results

    def parse(self):
        self.parse_requests()
        self.extract_keys()
        self.get_nested_items()
        self.get_unnested_items()

    def parse_requests(self):
        # First operation, to parse requests text into python dictionnaries
        for page, value in self.results.items():
            self.parsed[page] = json.loads(value.text)

    def get_nested_items(self):
        """
        Result is a dictionary, of one key: item_name, and value is list of items (concatenate all result pages).
        """
        dictionnary = {self.item_name: []}
        for page, value in self.parsed.items():
            # concatenate two lists of items
            dictionnary[self.item_name] += value[self.item_name]
        self.nested_items = dictionnary

    def get_unnested_items(self):
        df = pd.DataFrame(self.nested_items[self.item_name])
        flatten_dataframe(df, drop=True, max_depth=5)
        self.unnested_items = df.to_dict()

    def extract_keys(self):
        self.keys = list(self.parsed.keys())

    def extract_disruptions_list(self):
        pass

    def explain(self):
        print("PARSING OF " + self.asked_path)
        print("Keys found: " + str(self.keys))
        print(self.item_name.capitalize() + " has " +
              str(len(self.unnested_items)) + " elements.")
