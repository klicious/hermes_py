import os

import constants

SHEET_TO_GID = {
    "houses": "0",
    "line table": "1173382764",
    "spotmar fees": "1501856274",
    "swap fees": "1328136274",
    "confirmation methods": "1264120230",
    "swap trade sheet": "1309775153",
    "swap daily": "631563425",
    "swap log": "1994060119",
    "spotmar trade sheet": "535688668",
    "spotmar daily": "1781531085",
    "spotmar log": "1575013703",
    "holidays kr": "789623918",
    "holidays us": "1881204821",
}
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "1zBRneL0s1T0DA_guUakPldHhQzFEWPEHKyOfAfbx0D0"

GOOGLE_DIR = os.path.join(constants.RESOURCE_DIR, "google")
