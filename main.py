#!/usr/bin/python3
import os

from API.api_request import ApiRequest, RequestParser
from configuration import USER

# All main requests (missing some)
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
        # Write request log
        request.write_log(directory)
        if not request.first_request_status:
            # If first request failed, no parsing, go to next element
            request.write_log(directory)
            continue
        # Parse results if sucessful
        parser = RequestParser(request.results, requested_path)
        parser.parse()
        # Print some information
        parser.explain()
        # Write it on disk
        parser.write_all(directory)


etl_sncf(api_paths_list[14:], page_limit=1000, count=300, debug=True)
