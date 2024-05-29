from datetime import datetime

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
    for club in clubs:
        if request.form['email'] == club['email']:
            return render_template('welcome.html', club=club, competitions=competitions)
    flash("Sorry, that email wasn't found.")
    return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    competitions = loadCompetitions()
    clubs = loadClubs()

    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    today_date = datetime.timestamp(datetime.now())
    competition_date = datetime.timestamp(datetime.strptime(
        foundCompetition['date'], '%Y-%m-%d %H:%M:%S'))

    if foundClub and foundCompetition:
        if competition_date < today_date:
            flash("Error, this competitions has already ended.")
            return render_template('welcome.html', club=foundClub, competitions=competitions)
        else:
            flash("This competitions is still available")
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=foundClub, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competitions = loadCompetitions()
    clubs = loadClubs()
    competition = [c for c in competitions if c['name']
                   == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired > 12:
        flash('You can\'t book more than 12 places')

        return render_template('booking.html', club=club, competition=competition)

    elif placesRequired > int(club['points']):
        flash(f'You didn\'t have enough points to redeems '
              f'{placesRequired} places, you only have {int(club['points'])}')

        return render_template('booking.html', club=club, competition=competition)

    else:
        competition['numberOfPlaces'] = str(int(
            competition['numberOfPlaces'])-placesRequired)
        club['points'] = str(int(club['points'])-placesRequired)
        writeCompetitions(competitions)
        writeClubs(clubs)
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/showPointBoard')
def pointBoard():
    clubs = loadClubs()
    pointboard = []
    for club in clubs:
        pointboard.append({"name": club["name"], "points": club["points"]})
    return render_template('pointboard.html', pointboard=pointboard)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
