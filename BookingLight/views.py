from flask import Flask, render_template, request, redirect, flash, url_for

from .models import loadCompetitions, writeCompetitions, loadClubs, writeClubs

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    competitions = loadCompetitions()
    clubs = loadClubs()
    club = [club for club in clubs if club['email']
            == request.form['email']][0]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    competitions = loadCompetitions()
    clubs = loadClubs()
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competitions = loadCompetitions()
    clubs = loadClubs()
    competition = [c for c in competitions if c['name']
                   == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired > int(club['points']):
        return render_template('booking.html', club=club, competition=competition)
    else:
        competition['numberOfPlaces'] = str(int(
            competition['numberOfPlaces'])-placesRequired)
        club['points'] = str(int(club['points'])-placesRequired)
        writeCompetitions(competitions)
        writeClubs(clubs)
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
