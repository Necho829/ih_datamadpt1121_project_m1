import argparse
import pandas as pd
import geo_calculations as geo
from fuzzywuzzy import fuzz
import analyzing
import reporting

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--action",
        help="Define what you want to do.",
        choices=["closest-bike-location", "closest-bike-all"],
        required=True,
    )

    parser.add_argument(
        "--organization-name",
        help="Provide the org name.",
        dest="org_name",
    )

    parser.add_argument(
        "--output-format",
        help="Choose how to generate the data.",
        choices=["print", "csv"],
        dest="output_format",
        required=True,
    )

    parser.add_argument(
        "--fuzzy",
        help="Set flag if searching for location using fuzzy match",
        action="store_true",
    )

    args = parser.parse_args()
    if args.action == "closest-bike-all":
        data = analyzing.get_closest_bike_to_all()
        suffix = "all"
    elif args.action == "closest-bike-location":
        data = analyzing.get_closest_bike_to_location(args.org_name, args.fuzzy)
        suffix = args.org_name

    if data is not None:
        if args.output_format == "csv":
            filename = "./output_files/{}-{}.csv".format(args.action, suffix)
            reporting.generate_csv(data, filename)
            print("The output file has been generated under {}".format(filename))
        else:
            print(data.to_markdown())