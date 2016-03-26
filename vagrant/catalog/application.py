from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Book, User
import json
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///booklistingsapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Route for login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# This route handles logging in via Google+
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # Error handling codes.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    # Check for user already signed-in
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Store user data is session
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    flash("you are now logged in as %s" % login_session['username'])
    return "Redirecting..."


# Disconnect from Google+
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session[
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash('Successfully disconnected.')
        return redirect(url_for('showGenres'))
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        flash(response)
        return redirect(url_for('showGenres'))


# JSON APIs
@app.route('/genre/<int:genre_id>/books/JSON')
def genreBooksJSON(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    books = session.query(Book).filter_by(
        genre_id=genre_id).all()
    return jsonify(Books=[i.serialize for i in books])


@app.route('/genre/<int:genre_id>/books/<int:book_id>/JSON')
def bookJSON(genre_id, book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return jsonify(book=book.serialize)


@app.route('/genre/JSON')
def genresJSON():
    genres = session.query(Genre).all()
    return jsonify(genres=[r.serialize for r in genres])


# Show all genres
@app.route('/')
@app.route('/genres')
def showGenres():
    genres = session.query(Genre).all()
    return render_template('genres.html', genres=genres)


# Future addition, new, edit and delete categories with cascading in database.
# About page route
@app.route('/about')
def showAbout():
    return render_template('about.html')


# Show all books for a particular genre
@app.route('/genre/<int:genre_id>/')
@app.route('/genre/<int:genre_id>/books')
def showBooks(genre_id):
    # return "This page shows all the books for a particular genre"
    genres = session.query(Genre).all()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    books = session.query(Book).filter_by(genre_id=genre_id) 
    creator = getUserInfo(genre.user_id)
    if 'username' not in login_session:
    	return render_template('allbooks.html', genre_id=genre_id, genre=genre, books=books, genres=genres)
    else:
    	return render_template('books.html', genre_id=genre_id, genre=genre, books=books, genres=genres)



# Add a new book to a genre
@app.route('/genre/<int:genre_id>/books/new', methods=['GET', 'POST'])
def newBook(genre_id):
    # return "This page allows authenticated users to create a new item"
    if 'username' not in login_session:
        return redirect('/login')
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if request.method == 'POST':
        newBook = Book(name=request.form['name'], description=request.form[
            'description'], price=request.form['price'], author=request.form['author'], genre_id=genre_id, user_id=login_session['user_id'])
        session.add(newBook)
        flash('New Book %s Successfully Added' % newBook.name)
        session.commit()
        return redirect(url_for('showBooks', genre_id=genre_id))
    else:
        return render_template('newbook.html', genre_id=genre_id, genre=genre)


# Edit an existing book
@app.route('/genre/<int:genre_id>/books/<int:book_id>/edit', methods=['GET', 'POST'])
def editBook(genre_id, book_id):
    # return "This page allows authenticated users to edit an item"
    if 'username' not in login_session:
        return redirect('/login')
    editedBook = session.query(Book).filter_by(id=book_id).one()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if editedBook.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('Error: You are not authorized to edit this book.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedBook.name = request.form['name']
        if request.form['description']:
            editedBook.description = request.form['description']
        if request.form['price']:
            editedBook.price = request.form['price']
        if request.form['author']:
            editedBook.author = request.form['author']
        session.add(editedBook)
        flash('Book %s Successfully Edited' % editedBook.name)
        session.commit()
        return redirect(url_for('showBooks', genre_id=genre_id))
    else:
        return render_template('editbook.html', genre_id=genre_id, book=editedBook, genre=genre)


# Delete an existing book
@app.route('/genre/<int:genre_id>/books/<int:book_id>/delete', methods=['GET', 'POST'])
def deleteBook(genre_id, book_id):
    # return "This page allows authenticated users to delete an item"
    if 'username' not in login_session:
        return redirect('/login')
    bookToDelete = session.query(Book).filter_by(id=book_id).one()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if bookToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('Error: You are not authorized to delete this book.');}</script><body onload='myFunction()''>"    
    if request.method == 'POST':
        session.delete(bookToDelete)
        flash('Book %s Successfully Deleted' % bookToDelete.name)
        session.commit()
        return redirect(url_for('showBooks', genre_id=genre_id))
    else:
        return render_template('deletebook.html', genre_id=genre_id, book=bookToDelete, genre = genre)

# These helper functions are used to handle the User table in the db
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# Change key for actual deployment
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    # app.debug = True
    app.run(host='0.0.0.0', port=8000)
