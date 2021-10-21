import csv
import json
import sys


def json2csv(json_path, csv_path):
    with open(json_path) as fp:
        data = json.load(fp)

    fields = data[0].keys()

    with open(csv_path, "w") as fp:
        dw = csv.DictWriter(fp, fields)
        dw.writerows(data)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: python3 json2csv.py JSON_FILE CSV_FILE")
        sys.exit(1)

    json_path = sys.argv[1]
    csv_path = sys.argv[2]

    json2csv(json_path, csv_path)
