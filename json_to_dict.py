__author__ = 'patin_000'
'''Takes a web page containing json and returns a formatted dictionary.
   supports usr agent spoofing to get around cloud flare'''

# Imports, all standard libraries.

from json import loads
import urllib



def grab_json(url, spoof):

    if spoof:
        request = urllib.request.urlopen()
    raw_url_data = urllib.urlopen(url).read()
    return loads(raw_url_data)


if __name__ == "__main__":
    grab_json("http://fantasy.na.lolesports.com/en-US/api/season/4")