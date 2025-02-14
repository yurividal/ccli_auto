import requests
from get_cookies_and_token import get_cookie_and_token
import variables
import json

type = "lyrics"  # lyrics or sheetmusic


def get_history(Cookie):
    print("Attempting to get report history...")

    # Define the URL
    url = "https://reporting.ccli.com/api/history/" + type + "?lastMonthRange=3"

    # Define the headers from the raw capture
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://reporting.ccli.com/",
        "Content-Type": "application/json;charset=utf-8",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Te": "trailers",
        "Cookie": "(" + Cookie + ")",
    }

    # Send the GET request
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print(f"Error: {e}")
        return None

    if response.status_code == 200:
        return response.json()
    else:
        print("Error getting history")
        return None


def delete_report(report_id, Cookie, RequestVerificationToken):
    print(f"Deleting report with ID: {report_id}")

    # Define the URL for the DELETE request
    url = f"https://reporting.ccli.com/api/report/{type}/{report_id}"

    # Define the headers (assuming the same headers are valid for the DELETE request)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://reporting.ccli.com/",
        "Content-Type": "application/json;charset=utf-8",
        "RequestVerificationToken": RequestVerificationToken,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Te": "trailers",
        "Cookie": "(" + Cookie + ")",
    }

    # Send the DELETE request
    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print(f"Successfully deleted report {report_id}")

        else:
            print(f"Failed to delete report {report_id}: {response.status_code}")
    except Exception as e:
        print(f"Error deleting report {report_id}: {e}")


def process_reports(json_data, Cookie, RequestVerificationToken):
    data = json_data

    # Iterate over each song in the data array
    for song_data in data["data"]:
        # Iterate over each report in the song's data
        for report in song_data["data"]:
            report_id = report["reportId"]
            # Call the delete function for each report
            delete_report(report_id, Cookie, RequestVerificationToken)


RequestVerificationToken, Cookie = get_cookie_and_token()

history = get_history(Cookie)

process_reports(history, Cookie, RequestVerificationToken)
