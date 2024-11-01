import requests
from cookie_extractor import gui_login
from get_cookies_and_token import get_cookie_and_token
import variables


class Song:
    def __init__(self, ccli_number, song_id, title):
        self.ccli_number = ccli_number
        self.song_id = song_id
        self.title = title

    def __repr__(self):
        return f"{self.ccli_number} - {self.title} - {self.song_id}"


def search(song_ccli, Cookie, songs_dict):

    url_search = "https://reporting.ccli.com/api/search"

    params = {
        "searchTerm": song_ccli,
        "searchCategory": "all",
        "searchFilters": "[]",
    }

    headers_search = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Client-Locale": "en-GB",
        "Content-Type": "application/json;charset=utf-8",
        "Referer": "https://reporting.ccli.com/search?s="
        + song_ccli
        + "&page=1&category=all",
        "Cookie": "(" + Cookie + ")",
    }

    print("Getting details for song with CCLI number: ", song_ccli)
    response_search = requests.get(url_search, params=params, headers=headers_search)

    if response_search.status_code == 200:
        data = response_search.json()
        # print(data)
        for song_data in data["results"]["songs"]:
            ccli_number = song_data["ccliSongNo"]
            song_id = song_data["id"]
            title = song_data["title"]

            # Create a Song object with CCLI number, id, and title
            song = Song(ccli_number, song_id, title)
            # Add the Song object to the dictionary with CCLI as the key
            songs_dict[ccli_number] = song
    elif response_search.status_code == 401:
        print(
            "Error submitting report, HTTP Response Code: 401, Probably bad Cookie. \n Script will now delete the current token and cookies \n Please run the script again to get new token and cookies."
        )

        import os

        try:
            os.remove("RequestVerificationToken.txt")
            os.remove("Cookie.txt")
        except:
            pass

    else:
        print("Error: ", response_search.status_code)


def report(songs_dict, Cookie, RequestVerificationToken):

    data = {
        "songs": [],
        "lyrics": {"uses": 1, "digital": 0, "print": 0, "record": 0, "translate": 0},
        "sheetMusic": [],
        "rehearsals": [],
        "mrsls": [],
    }

    for song in songs_dict.values():
        # Create a dictionary for each song
        song_entry = {
            "id": song.song_id,
            "title": song.title,
            "ccliSongNo": song.ccli_number,
        }
        # Append the song to the "songs" list in the data
        data["songs"].append(song_entry)

    totalNumberOfSongs = len(data["songs"])

    first_song = next(iter(songs_dict.values()))

    url_report = "https://reporting.ccli.com/api/report"
    headers_post = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/json",
        "RequestVerificationToken": RequestVerificationToken,
        "Client-Locale": "en-GB",
        "Origin": "https://reporting.ccli.com",
        "Referer": "https://reporting.ccli.com/search?s="
        + first_song.ccli_number
        + "&page=1&category=all",
        "Cookie": "(" + Cookie + ")",
    }

    response_post = requests.post(url_report, json=data, headers=headers_post)

    if response_post.status_code == 200:

        print("\n" + str(totalNumberOfSongs) + " songs reported successfully.")
    elif response_post.status_code == 409:
        print(
            "Error submitting report, HTTP Response Code: 409, Probably bad RequestVerificationToken. \n Script will now delete the current token and cookies \n Please run the script again to get new token and cookies."
        )

        import os

        try:
            os.remove("RequestVerificationToken.txt")
            os.remove("Cookie.txt")
        except:
            pass
    elif response_post.status_code == 401:
        print(
            "Error submitting report, HTTP Response Code: 401, Probably bad Cookie. \n Script will now delete the current token and cookies \n Please run the script again to get new token and cookies."
        )

        import os

        try:
            os.remove("RequestVerificationToken.txt")
            os.remove("Cookie.txt")
        except:
            pass
    else:
        print("Error submitting report:", response_post.status_code, response_post.text)


def main():
    song_list = variables.song_list
    # if (len(song_list)) < 2:
    #     print(
    #         "Looks like only one song in the list. No need to automate anything else. Exiting."
    #     )
    #     exit()

    RequestVerificationToken, Cookie = get_cookie_and_token()

    songs_dict = {}

    for song in song_list:
        search(song, Cookie, songs_dict)

    for song in songs_dict.values():
        print(song)

    report(songs_dict, Cookie, RequestVerificationToken)


if __name__ == "__main__":
    main()
