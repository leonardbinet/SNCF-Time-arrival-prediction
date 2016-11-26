#!/usr/bin/python3
import os
import pandas as pd
import json

from API.api_request import ApiRequest, RequestParser
from API.utils import flatten_columns, flatten_dataframe, flattenjson
from configuration import USER

# EXAMPLE
# possible requests
# api_path = "coverage/sncf/lines"
api_paths_list = [
    'coverage/sncf/addresses',
    'coverage/sncf/contributors',
    'coverage/sncf/companies',
    'coverage/sncf/connections',
    'coverage/sncf/vehicle_journeys',  # flatten diff keys?
    'coverage/sncf/networks',
    'coverage/sncf/commercial_modes',
    'coverage/sncf/physical_modes',
    'coverage/sncf/disruptions',
    'coverage/sncf/pois',
    'coverage/sncf/stop_points',
    'coverage/sncf/poi_types',
    'coverage/sncf/datasets',
    'coverage/sncf/journey_pattern_points',
    'coverage/sncf/lines',
    'coverage/sncf/coord',
    'coverage/sncf/stop_areas',
    'coverage/sncf/coords',
    'coverage/sncf/journey_patterns',
    'coverage/sncf/routes',
    'coverage/sncf/trips',
    'coverage/sncf/line_groups',
    'coverage/sncf/places',
    'coverage/sncf/journeys'
]


def etl_sncf(api_paths, page_limit=100, count=100, debug=False):
    for requested_path in api_paths:
        # Create Data directory if it doesn't exist
        directory = os.path.join("Data", requested_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Compute request
        request = ApiRequest(USER, requested_path)
        request.compute_request_pages(
            page_limit=page_limit, debug=debug, count=count)
        print(request.total_result)
        if not request.first_request_status:
            continue
        # Parse results if sucessful
        parser = RequestParser(request.results, requested_path)
        parser.parse()
        parser.explain()
        # Get results
        unnested = pd.DataFrame(parser.unnested_items)  # df
        nested = parser.nested_items  # dict
        # Write results
        # Write csv
        unnested.to_csv(os.path.join(directory, parser.item_name + ".csv"))
        # Write json
        with open(os.path.join(directory, parser.item_name + ".json"), 'w') as f:
            json.dump(nested, f, ensure_ascii=False)

etl_sncf(api_paths_list, page_limit=1000, count=100, debug=True)
