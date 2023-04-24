import pandas as pd
import re

def parse_raw_response(raw_response):
    is_string = isinstance(raw_response, str)
    string_response = str(raw_response) if not is_string else raw_response
    matches = re.findall("[12]", string_response)

    # Count the number of occurrences of 1 and 2
    count_1 = matches.count("1")
    count_2 = matches.count("2")

    if not isinstance(count_1, int) or not isinstance(count_2, int):
        return 'err'
    elif count_2 == 0:
        return 1
    elif count_1 == 0:
        return 2
    else:
        return 'err'

# Read in output/rekt.csv file
df = pd.read_csv("./output/rekt.csv",index_col=0)
df['kill'] = df['response'].apply(parse_raw_response)
df.to_csv("./output/parsed_data.csv",header=True)