from API.api_request import compute_api_request
from configuration import USER

# possible requests
# path = "coverage/sncf/lines"
# path = "coverage/sncf/stop_points"

path = "coverage/sncf/disruptions"
result = compute_api_request(path, USER)
