import json
import urllib.request
import requests
import os

def addtxt(text, title="file.txt"):
    """ Ajoute du text sur ipfs """

    params = {
        'quiet': 'true',
        'pin': 'true'
    }

    files = {
        'file': (title, text)
    }

    r = requests.post('https://ipfs.oversas.org/api/v0/add', params=params, files=files)

    return r.json()


def addfile(path):
    """ Ajoute un fichier sur ipfs """

    if os.path.isfile(path) == False:

        return False

    params = {
        'quiet': 'true',
        'pin': 'true'
    }

    files = {
        'file': open(path, 'rb'),
    }

    r = requests.post('https://ipfs.oversas.org/api/v0/add', params=params, files=files)

    return r.json()


def getfile(hash):

    url = "https://ipfs.oversas.org/api/v0/cat"

    payload = {"arg": hash}

    r = requests.get(url, params=payload)

    try:

        return r.json()

    except BaseException:

        return r.text
