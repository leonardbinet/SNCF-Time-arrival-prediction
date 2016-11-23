import pandas as pd
import json

from API.api_request import compute_api_request
from API.utils import flatten_columns, flatten_dataframe
from configuration import USER

# EXAMPLE
# possible requests
# path = "coverage/sncf/lines"
# path = "coverage/sncf/stop_points"
api_path = "coverage/sncf/disruptions"

result = compute_api_request(api_path, USER, page_limit=5)
df = result["disruptions"]
created_cols = flatten_dataframe(df, True, 5)

print("-" * 30)
print("Created columns during flatenning:\n ", created_cols)
print(df.head(5))

path_to_save = "example.csv"
df.to_csv(path_to_save)
print("Dataframe save in csv format in " + path_to_save)
