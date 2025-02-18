from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for

from .models import loadCompetitions, writeCompetitions, loadClubs, writeClubs

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def index():
    """home page with the login"""

    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    """take the email to redirect the welcome page with the list of competitions"""

    competitions = loadCompetitions()
    clubs = loadClubs()

    for club in clubs:
        if request.form['email'] == club['email']:
            return render_template('welcome.html', club=club, competitions=competitions)
    flash("Sorry, that email wasn't found.")
    return render_template('index.html')


@app.route('/book/<competition_name>/<club_name>')
def book(competition_name, club_name):
    """take the selected competition to redirect to the booking page
    where whe will give the number of place to reedem"""

    competitions = loadCompetitions()
    clubs = loadClubs()

    foundClub = []
    foundCompetition = []
    for competition in competitions:
        if competition['name'] == competition_name:
            foundCompetition = competition
            break
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=foundClub, competitions=competitions)

    for club in clubs:
        if club['name'] == club_name:
            foundClub = club
            break
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=foundClub, competitions=competitions)

    today_date = datetime.timestamp(datetime.now())
    competition_date = datetime.timestamp(datetime.strptime(
        foundCompetition['date'], '%Y-%m-%d %H:%M:%S'))

    if competition_date < today_date:
        flash("Error, this competitions has already ended.")
        return render_template('welcome.html', club=foundClub, competitions=competitions)
    else:
        flash("This competitions is still available")
        return render_template('booking.html', club=foundClub, competition=foundCompetition)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """take the number of place to redeem to check if valide and redirect to the welcome page if all good"""

    competitions = loadCompetitions()
    clubs = loadClubs()
    this_competition = {}
    this_club = {}

    for competition in competitions:
        if competition['name'] == request.form['competition']:
            this_competition = competition
            break
    else:
        flash("Something went wrong")
        return render_template('index.html')

    for club in clubs:
        if club['name'] == request.form['club']:
            this_club = club
            break

    else:
        flash("Something went wrong")
        return render_template('index.html')

    placesRequired = int(request.form['places'])
    if placesRequired > 12:
        flash('You can\'t book more than 12 places')

        return render_template('booking.html', club=this_club, competition=this_competition)

    elif placesRequired > int(this_club['points']):
        flash(f'You didn\'t have enough points to redeems '
              f'{placesRequired} places, you only have {int(this_club['points'])}')

        return render_template('booking.html', club=this_club, competition=this_competition)

    else:
        this_competition['numberOfPlaces'] = str(int(
            this_competition['numberOfPlaces'])-placesRequired)
        this_club['points'] = str(int(this_club['points'])-placesRequired)
        writeCompetitions(competitions)
        writeClubs(clubs)
        flash('Great-booking complete!')
        return render_template('welcome.html', club=this_club, competitions=competitions)


@app.route('/showPointBoard')
def pointBoard():
    """redirect to the pointboard to see the point of each club"""

    clubs = loadClubs()

    pointboard = []
    for club in clubs:
        pointboard.append({"name": club["name"], "points": club["points"]})
    return render_template('pointboard.html', pointboard=pointboard)


@app.route('/logout')
def logout():
    """redirect to the home page"""

    return redirect(url_for('index'))
