# encoding: utf-8
"""
gender_io.py
"""
import requests
import json


def get_genders(names):
    """Create a call to genderize for up to 10 names in a list."""
    url = ""
    cnt = 0
    if not isinstance(names, list):
        names = [names, ]

    for name in names:
        if url == "":
            url = "name[0]=" + name
        else:
            cnt += 1
            url = url + "&name[" + str(cnt) + "]=" + name

    # provide your own api key
    f = open('genderize_api_key.txt', 'r')
    key = f.read().strip()
    f.close()
    api_key = 'apikey=' + key + '&'
    req = requests.get("http://api.genderize.io?" + api_key + url)
    results = json.loads(req.text)
    if len(names) == 1:
        results = [results, ]

    retrn = []
    for result in results:
        if result["gender"] is not None:
            retrn.append((result["gender"], result["probability"],
                          result["count"]))
        else:
            retrn.append((u'None', u'0.0', 0.0))
    return retrn
