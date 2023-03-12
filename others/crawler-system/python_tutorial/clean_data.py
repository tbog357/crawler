import os
import json
import pandas as pd
from io import StringIO

if __name__ == "__main__":
    folder = os.listdir("raw_data")
    raw_data = []
    for file in folder:
        path = os.path.join("raw_data", file)

        raw_data.append(json.load(open(path, "r")))

    tables = []
    for idx, data in enumerate(raw_data):
        df = pd.read_csv(StringIO(data["resp"]))
        df.to_csv(f"raw_data/{idx}.csv", index=False)
