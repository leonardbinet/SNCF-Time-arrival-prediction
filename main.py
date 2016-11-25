import os
import pandas as pd
import json

from API.api_request import compute_api_request
from API.utils import flatten_columns, flatten_dataframe
from configuration import USER

# EXAMPLE
# possible requests
# api_path = "coverage/sncf/lines"
api_paths = [
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


for i in range(len(api_paths)):
    # Create Data directory if it doesn't exist
    if not os.path.exists(os.path.join("Data", api_paths[i])):
        os.makedirs(os.path.join("Data", api_paths[i]))
    # Compute api requests, with limit of 5 pages
    result = compute_api_request(api_paths[i], USER, page_limit=5)
    # We keep only the items
    df = result["items"]
    # We flatten the dataframe
    created_cols = flatten_dataframe(df, True, 5)
    # We save it (in Data folder)
    df.to_csv(os.path.join("Data", api_paths[i], "items.csv"))
