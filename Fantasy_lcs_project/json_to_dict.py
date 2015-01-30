__author__ = 'patin_000'
'''Takes a web page containing json and returns a formatted dictionary.
   supports usr agent spoofing to get around cloud flare'''

# Imports, all standard libraries.

from json import loads
import urllib2



def grab_json(url, spoof):

    if spoof:
        headers = {"User-Agent" : "Mozilla/5.0"}
        request = urllib2.Request(url,None,headers)
        html = urllib2.urlopen(request).read()
        return loads(html)
    else:
        raw_url_data = urllib2.urlopen(url).read()
        return loads(raw_url_data)


if __name__ == "__main__":
    test = grab_json("http://fantasy.na.lolesports.com/en-US/api/season/4",True)