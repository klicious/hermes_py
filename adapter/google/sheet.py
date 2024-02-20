from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from . import authentication
from . import constants


def get_gid(sheet_name: str):
    return constants.SHEET_TO_GID.get(sheet_name.lower())


def get_values(sheet_name: str, _range: str):
    try:
        creds = authentication.get_credentials()
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(
                spreadsheetId=constants.SPREADSHEET_ID, range=f"'{sheet_name}'!{_range}"
            )
            .execute()
        )
        return result.get("values", [])
    except HttpError as err:
        print(err)
