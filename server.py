from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from booking import confirmation_message, parse_places, validate_purchase
from club import MAX_PLACES, find_by_email, find_by_name as find_club_by_name
from competition import find_by_name as find_competition_by_name
from competition import upcoming
from config import secret_key
from repository import (
    load_clubs,
    load_competitions,
    save_clubs,
    save_competitions,
)


app = Flask(__name__)
app.secret_key = secret_key()

competitions = load_competitions()
clubs = load_clubs()


def club_de_session():
    email = session.get('email')
    if email is None:
        return None
    return find_by_email(clubs, email)


def refuser_sans_session():
    flash('Sorry, you must be logged in.')
    return redirect(url_for('index'))


def competitions_a_venir():
    return upcoming(competitions)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = find_by_email(clubs, request.form.get('email', ''))
    if club is None:
        flash('Sorry, that email is not registered.')
        return render_template('index.html'), 200
    session['email'] = club['email']
    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions_a_venir(),
    )


@app.route('/book/<competition>/<club>')
def book(competition, club):
    clubSession = club_de_session()
    if clubSession is None:
        return refuser_sans_session()
    foundClub = find_club_by_name(clubs, club)
    foundCompetition = find_competition_by_name(competitions, competition)
    if foundClub is None or foundCompetition is None:
        flash("Sorry, this club or competition does not exist.")
        return redirect(url_for('index'))
    if foundClub['name'] != clubSession['name']:
        flash("Sorry, you cannot book for another club.")
        return redirect(url_for('index'))
    return render_template(
        'booking.html',
        club=foundClub,
        competition=foundCompetition,
        max_places=MAX_PLACES,
    )


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    clubSession = club_de_session()
    if clubSession is None:
        return refuser_sans_session()
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
    if foundClub['name'] != clubSession['name']:
        flash("Sorry, you cannot book for another club.")
        return redirect(url_for('index'))

    error = validate_purchase(foundClub, foundCompetition, placesRequired)
    if error is not None:
        flash(error)
        return render_template(
            'welcome.html',
            club=foundClub,
            competitions=competitions_a_venir(),
        )

    foundCompetition['numberOfPlaces'] = int(foundCompetition['numberOfPlaces'])-placesRequired
    foundClub['points'] = int(foundClub['points'])-placesRequired
    save_clubs(clubs)
    save_competitions(competitions)
    flash(confirmation_message(placesRequired))
    return render_template(
        'welcome.html',
        club=foundClub,
        competitions=competitions_a_venir(),
    )


# TODO: Add route for points display


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))
