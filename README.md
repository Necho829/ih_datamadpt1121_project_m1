###PROJECT 1 "BICIMADADRID"
Quick implementation of this project

Environment:
Python3.8

How to run in command line:

Shortest distance to all
CSV
python main.py --action closest-bike-all --output-format csv 

Print
python main.py --action closest-bike-all --output-format print

Get shortest distance to a specific location:
Replace "Zapadores Ciudad del Arte" with your desired location

CSV
python pipeline_main.py --action closest-bike-location --output-format csv --organization-name "Zapadores Ciudad del Arte"

Print
python pipeline_main.py --action closest-bike-location --output-format print --organization-name "Zapadores Ciudad del Arte"

Get shortest distance to a location using fuzzy matching
We've implemented the option to search for a location using fuzzy matching (Token Sort Ratio) on its name. The score threshold has been set to 80, can be change as needed. Use the below example to see it at work

CSV
python pipeline_main.py --action closest-bike-location --output-format csv --organization-name "Monasterio de la encarnacion" --fuzzy

Print
python pipeline_main.py --action closest-bike-location --output-format print --organization-name "Monasterio de la encarnacion" --fuzzy