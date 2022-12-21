import json
import urllib.request
import requests
import os


def addtxt(text, title="file.txt"):
    """ Ajoute du text sur ipfs """

    url = "https://oversas.org/api/v0/add"

    files = {'file': (title, text)}

    r = requests.post(url, files=files)

    return r.json()


def addfile(path):
    """ Ajoute un fichier sur ipfs """

    if os.path.isfile(path) == False:

        return False

    url = "https://oversas.org:5001/api/v0/add"

    params = (('pin', 'false'), ('recursive', 'true'))

    files = {'file': (path, open(path, 'rb'))}

    r = requests.post(url, files=files, params=params)

    return r.json()


def getfile(hash):

    url = "https://oversas.org/api/v0/cat"

    payload = {"arg": hash}

    r = requests.get(url, params=payload)

    try:

        return r.json()

    except BaseException:

        return r.text
