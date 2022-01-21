import pandas as pd
import requests
import geo_calculations as geo
from fuzzywuzzy import fuzz

def load_cc():
    
    cultural_centers = requests.get(
        "https://datos.madrid.es/egob/catalogo/200304-0-centros-culturales.json"
    )
    cultural_centers = cultural_centers.json()
    df_cultural_centers = pd.json_normalize(cultural_centers["@graph"])
    df_cultural_centers = pd.DataFrame(
        df_cultural_centers[
            [
                "organization.organization-name",
                "address.street-address",
                "location.latitude",
                "location.longitude",
            ]
        ]
    )
    df_cultural_centers = df_cultural_centers.assign(
        center_type="Centros culturales"
    )
    return df_cultural_centers


def load_museums():
    museums = requests.get("https://datos.madrid.es/egob/catalogo/201132-0-museums.json")
    museums = museums.json()
    df_museums = pd.json_normalize(museums["@graph"])
    df_museums = pd.DataFrame(
        df_museums[
            [
                "organization.organization-name",
                "address.street-address",
                "location.latitude",
                "location.longitude",
            ]
        ]
    )
    df_museums = df_museums.assign(center_type="museos")
    return df_museums

def load_data_bicimad():
    df_bicimad_stations = pd.read_json("../Database/bicimadstations.json")
    lon = [
        float(index["geometry_coordinates"].split(",")[0].replace("[", ""))
        for row, index in df_bicimad_stations.iterrows()
    ]
    lat = [
        float(index["geometry_coordinates"].split(",")[1].replace("]", ""))
        for row, index in df_bicimad_stations.iterrows()
    ]
    df_bicimad_stations["latitude"] = lat
    df_bicimad_stations["longitude"] = lon
    df_bicimad_stations= pd.DataFrame(
        df_bicimad_stations[["name", "address", "latitude", "longitude"]]
    )
    
    df_bicimad_stations["coordinates_mercator"] = df_bicimad_stations.apply(
        lambda x: geo.to_mercator(x["latitude"], x["longitude"]), axis=1
    )
    return df_bicimad_stations