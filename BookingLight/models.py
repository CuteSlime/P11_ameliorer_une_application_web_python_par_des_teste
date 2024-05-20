import json

url = './BookingLight/'


def loadClubs():
    with open(url + 'clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open(url + 'competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def writeClubs(clubs):
    with open(url + 'clubs.json', 'w') as club:
        json.dump({'clubs': clubs}, club, indent=4)


def writeCompetitions(competitions):
    with open(url + 'competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps, indent=4)
