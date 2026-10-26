from flask import Flask,render_template,request,redirect,flash,url_for

from booking import confirmation_message, parse_places, validate_purchase
from club import find_by_email, find_by_name as find_club_by_name
from competition import find_by_name as find_competition_by_name
from repository import load_clubs, load_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = find_by_email(clubs, request.form.get('email', ''))
    if club is None:
        flash('Sorry, that email is not registered.')
        return render_template('index.html'), 200
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = find_club_by_name(clubs, club)
    foundCompetition = find_competition_by_name(competitions, competition)
    if foundClub is None or foundCompetition is None:
        flash("Sorry, this club or competition does not exist.")
        return redirect(url_for('index'))
    return render_template('booking.html',club=foundClub,competition=foundCompetition)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    placesRequired = parse_places(request.form.get('places'))
    foundCompetition = find_competition_by_name(
        competitions, request.form.get('competition'))
    foundClub = find_club_by_name(clubs, request.form.get('club'))

    if placesRequired is None:
        flash("Sorry, the number of places is invalid.")
        return redirect(url_for('index'))
    if foundClub is None or foundCompetition is None:
        flash("Sorry, this club or competition does not exist.")
        return redirect(url_for('index'))

    error = validate_purchase(foundClub, foundCompetition, placesRequired)
    if error is not None:
        flash(error)
        return render_template('welcome.html', club=foundClub, competitions=competitions)

    foundCompetition['numberOfPlaces'] = int(foundCompetition['numberOfPlaces'])-placesRequired
    foundClub['points'] = int(foundClub['points'])-placesRequired
    flash(confirmation_message(placesRequired))
    return render_template('welcome.html', club=foundClub, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
