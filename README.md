# ccli_auto
Reports song usage to CCLI based on a list of song CCLI numbers

## How to Use:
- rename the file variables_example.py to variables.py
- edit it with your ccli username, password and a list of all the CCLI songs you want to report
- install the necessary python dependencies:
   ````
    pip install requests selenium
   ````
- run the main script:
  ````
  python auto_ccli.py
  ````

## How it works
CCLI doesn't have a public API for reporting, nor does it have any other method of authenticating a user to send requests to their servers. So, this script attempts to obtain your authentication cookies by opening a browser session, and observing your login headers.

Once the token and the authentication cookies are obtained, the script then proceeds to reporting the songs.

The script will automatically save the cookies and the token into a file, in order to skip login next time you hav to run it.

In order to report a song via API call, the server requires the CCLI id, the song id, and the offical song title.

The script automatically searches for these parameters for every one of the songs in the list, them submits a single usage report for each item in the list.


#### What if i already have the token and cookies?
If you want to manually obtain the Cookies and token, and not have to use selenium, you can simply edit the main script:
- Open a Browser session and login to CCLI.
- Open developer tools and go to the Network tab
- Then, search for any CCLI song, and report once.
- On the network tab, look for the POST request to the /api/report endpoint
- Look for the Request Headers and copy the RequestVerificationToken and Cookie values.
- Save their raw values into 2 files, on the folder where the script is located, with the following names:
  ````
  RequestVerificationToken.txt
  Cookie.txt
  ````

#### If you are doing testing and want to delete all the reports in the last 3 months, execute the delete_all.py script. 

