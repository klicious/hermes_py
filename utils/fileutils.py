import csv


def read_csv_to_dicts(file_path: str) -> list:
    """
    Reads a CSV file and parses its content into a list of dictionaries.

    :param file_path: The path to the CSV file.
    :return: A list of dictionaries, where each dictionary represents a row in the CSV, with keys being the column headers.
    """
    data = []
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        reader.fieldnames = [name.replace(" ", "_") for name in reader.fieldnames]
        for row in reader:
            data.append({k.strip(): v.strip() for k, v in row.items()})
    return data
