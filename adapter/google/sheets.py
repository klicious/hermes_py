from typing import List

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from . import authentication
from . import constants


def service():
    creds = authentication.get_credentials()
    return build("sheets", "v4", credentials=creds).spreadsheets()


def get_spreadsheet():
    try:
        return service().get(spreadsheetId=constants.SPREADSHEET_ID).execute()
    except HttpError as err:
        print(err)


def get_gid(sheet_name: str):
    return constants.SHEET_TO_GID.get(sheet_name.lower())


def get_values(sheet_name: str, _range: str):
    result = (
        service()
        .values()
        .get(spreadsheetId=constants.SPREADSHEET_ID, range=f"'{sheet_name}'!{_range}")
        .execute()
    )
    return to_dict(result.get("values", []))


def to_dict(sheet_values: List[List[str]]):
    columns = sheet_values[0]
    return [
        {columns[i].replace(" ", "_"): value for i, value in enumerate(row)}
        for row in sheet_values[1:]
    ]
