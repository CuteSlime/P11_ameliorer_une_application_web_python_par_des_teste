import json

url = './BookingLight/'


def loadClubs():
    """read the Json file for clubs and return this content as a variable"""

    with open(url + 'clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    """read the Json file for competitions and return this content as a variable"""

    with open(url + 'competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def writeClubs(clubs):
    """"take the new list of clubs and overwrite the json file"""

    with open(url + 'clubs.json', 'w') as club:
        json.dump({'clubs': clubs}, club, indent=4)


def writeCompetitions(competitions):
    """"take the new list of competitions and overwrite the json file"""

    with open(url + 'competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps, indent=4)
