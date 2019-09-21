"""
BEFORE RUNNING:
---------------
1. If not already done, enable the Google Sheets API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/sheets
2. Install the Python client library for Google APIs by running
   `pip install --upgrade google-api-python-client`
"""
from pprint import pprint

from googleapiclient import discovery


def main(array):
    # https://developers.google.com/sheets/quickstart/python#step_3_set_up_the_sample
    #
    # Authorize using one of the following scopes:
    #     'https://www.googleapis.com/auth/drive'
    #     'https://www.googleapis.com/auth/drive.file'
    #     'https://www.googleapis.com/auth/spreadsheets'
    credentials = None

    service = discovery.build('sheets', 'v4', credentials=credentials)

    # The ID of the spreadsheet to update.
    spreadsheet_id = '1entWz5u4M0q0t1OqS7gsMNKuaGHUEzgfuxMjjKe2Qsc'

    # The A1 notation of a range to search for a logical table of data.
    # Values will be appended after the last row of the table.
    range_name = 'B:F'

    # How the input data should be interpreted.
    value_input_option = 'RAW'


    values = [array]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()


