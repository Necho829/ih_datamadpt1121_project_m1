import pandas as pd
import geo_calculations as geo
from fuzzywuzzy import fuzz
import acquisition

def load_data_organization():
    data = pd.concat([acquisition.load_cc(), acquisition.load_museums()])
    data["coordinates_mercator"] = data.apply(
        lambda x: geo.to_mercator(x["location.latitude"], x["location.longitude"]),
        axis=1,
    )
    return data

def find_organization_by_name(org_name, fuzzy):
    data = load_data_organization()
    if not fuzzy:
        try:
            org = data[data["organization.organization-name"] == org_name].iloc[0]
            return org
        except Exception as e:
            print("Organization not found!")
            return None
    else:  
        data["fuzzy_ratio"] = data.apply(
            lambda x: fuzz.token_sort_ratio(
                x["organization.organization-name"], org_name
            ),
            axis=1,
        )
        matched = data[data["fuzzy_ratio"] > 80]
        if not matched.empty:
            print(
                "{} organizations found using fuzzy match with close enough names".format(
                    len(matched)
                )
            )
            return matched.sort_values(by="fuzzy_ratio", ascending=False).iloc[0]
        else:
            print("No organization found using fuzzy match!")
            return None

def get_closest_bike(data_place, df_bikes):
    df_bikes["total_distance"] = df_bikes.apply(
        lambda x: x["coordinates_mercator"].distance(
            data_place["coordinates_mercator"]
        ),
        axis=1,
    )
    return df_bikes.sort_values(by="total_distance", ascending=True).iloc[0]
