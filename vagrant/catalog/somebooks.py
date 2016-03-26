from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Genre, Base, Book, User

engine = create_engine('sqlite:///booklistingsapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# This file adds dummy data to the database for testing. Note dummy user's
# data cannot be edited.

# Create dummy user
User1 = User(name="Enid", email="enid@example.com",
             picture='http://placecage.com/200/200')
session.add(User1)
session.commit()

# Create genres and books
genre1 = Genre(user_id=1, name="Sci-Fi")

session.add(genre1)
session.commit()

book1 = Book(user_id=1, name="Lord of the Rings", description="The ruler of the one ring beckons...",
             price="$7.50", author="JRR Tolkien", genre=genre1)

session.add(book1)
session.commit()


book2 = Book(user_id=1, name="Harry Potter", description="Wizards in a magic school!",
             price="$3.99", author="JK Rowling", genre=genre1)

session.add(book2)
session.commit()

book3 = Book(user_id=1, name="The Martian", description="When there is no Earth where do you go...",
             price="$5.50", author="Andy Weir", genre=genre1)

session.add(book3)
session.commit()


book4 = Book(user_id=1, name="Artemis Fowl", description="Get ready for a time travelling adventure.",
             price="$7.99", author="Eoin Colfer", genre=genre1)

session.add(book4)
session.commit()


# Book for Genre 2
genre2 = Genre(user_id=1, name="Non-Fiction")

session.add(genre2)
session.commit()


book1 = Book(user_id=1, name="Zero to One", description="From the founder of Paypal",
             price="$7.99", author="Peter Thiel", genre=genre2)

session.add(book1)
session.commit()

book2 = Book(user_id=1, name="Wings of Fire",
             description="The definitive book by the Indian President", price="$2.50", author="APJ Abdul Kalam", genre=genre2)

session.add(book2)
session.commit()


# Book for Genre 3
genre3 = Genre(user_id=1, name="Horror")

session.add(genre3)
session.commit()


book1 = Book(user_id=1, name="Goosebumps", description="Scary stories for kids",
             price="$8.99", author="R.L. Stine", genre=genre3)

session.add(book1)
session.commit()


# Book for Genre 4
genre1 = Genre(user_id=1, name="Children")

session.add(genre1)
session.commit()


book1 = Book(user_id=1, name="Famous Five", description="Best stories for children, timeless classic.",
             price="$2.99", author="Enid Blyton", genre=genre1)

session.add(book1)
session.commit()

# Book for Genre5
genre1 = Genre(user_id=1, name="Romance")

session.add(genre1)
session.commit()


book1 = Book(user_id=1, name="Shellfish Tower", description="Love on the beach until a twist!",
             price="$13.95", author="PT Moss", genre=genre1)

session.add(book1)
session.commit()

book2 = Book(user_id=1, name="To Die For", description="Love and mystery combine.",
             price="$22.95", author="PT Moss", genre=genre1)

session.add(book2)
session.commit()


# Book for Genre
genre1 = Genre(user_id=1, name="Modern")

session.add(genre1)
session.commit()

book1 = Book(user_id=1, name="Something Random", description="Random title!",
             price="$13.95", author="Miss Mok", genre=genre1)

session.add(book1)
session.commit()
book2 = Book(user_id=1, name="Something Abstrract", description="About art",
             price="$22.95", author="P DD", genre=genre1)

session.add(book2)
session.commit()


# Book for Genre
genre1 = Genre(user_id=1, name="Academic")

session.add(genre1)
session.commit()

book1 = Book(user_id=1, name="Math Instant", description="Algebra through pre-calculus.",
             price="$13.95", author="KK Mennon", genre=genre1)

session.add(book1)
session.commit()
book2 = Book(user_id=1, name="Science Daily", description="Mostly Bio and Chem.",
             price="$22.95", author="Kristy Bell", genre=genre1)

session.add(book2)
session.commit()


# Book for Genre
genre1 = Genre(user_id=1, name="Computer Science")

session.add(genre1)
session.commit()
book1 = Book(user_id=1, name="Learn Python", description="Flask, Django and more!",
             price="$13.95", author="AJ Miller", genre=genre1)

session.add(book1)
session.commit()
book2 = Book(user_id=1, name="Learn Web Dev", description="HTML, CSS and More...",
             price="$22.95", author="James Kimmel", genre=genre1)

session.add(book2)
session.commit()


print "added db items!"
