from textwrap import wrap
import pandas as pd
import geo_calculations as geo
from fuzzywuzzy import fuzz
import acquisition
import wrangling

def generate_relevant_df(data):
    relevant_cols = [
        "organization.organization-name",
        "center_type",
        "address.street-address",
        "bici_name",
        "bici_address",
        "bici_dist_total",
    ]
    data = data[relevant_cols]
    data = data.rename(
        columns={
            "organization.organization-name": "place_name",
            "center_type": "place_type",
            "address.street-address": "place_address",
            "bici_name": "bicimad_station",
            "bici_address": "station_location",
            "bici_dist_total": "distance",
        }
    )
    return data

def get_closest_bike_to_all():
    org_data = wrangling.load_data_organization()
    bike_data = acquisition.load_data_bicimad()
    org_data[
        [
            "bici_name",
            "bici_address",
            "bici_lat",
            "bici_lon",
            "bici_coordinates_mercator",
            "bici_dist_total",
        ]
    ] = org_data.apply(lambda x: wrangling.get_closest_bike(x, bike_data.copy()), axis=1)
    relevant_df = generate_relevant_df(org_data)
    return relevant_df


def get_closest_bike_to_location(org_name, fuzzy):
    location_data = wrangling.find_organization_by_name(org_name, fuzzy)
    if location_data is None:
        return
    bike_data = acquisition.load_data_bicimad()
    closest_bike = wrangling.get_closest_bike(location_data, bike_data)
    location_data["bici_name"] = closest_bike["name"]
    location_data["bici_address"] = closest_bike["address"]
    location_data["bici_dist_total"] = closest_bike["total_distance"]
    enriched_data = pd.DataFrame([location_data])
    relevant_df = generate_relevant_df(enriched_data)
    return relevant_df