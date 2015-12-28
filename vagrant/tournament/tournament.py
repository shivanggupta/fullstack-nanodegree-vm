#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM matches;")
    db.commit()
    cursor.close()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM players;")
    db.commit()
    cursor.close()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT count(*) FROM players;")
    count = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (%s) ;", (name,))
    db.commit()
    cursor.close()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place or a player
    tied for first place if there is currently a tie.

    Returns:
     A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT players.player_id, players.name, number_wins AS wins, number_matches AS matches FROM players, wins, count_matches WHERE players.player_id = wins.player_id AND players.player_id = count_matches.player_id ORDER BY number_wins DESC;")  # noqa
    standings = cursor.fetchall()
    cursor.close()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO matches (winner_id,loser_id) VALUES (%s, %s) ;", (winner, loser, ))
    db.commit()
    cursor.close()
    db.close()


def checkAndSubmitBye():
    """Returns player_id of the player who is awarded bye for the next round of a match.

    Assuming that there are an odd number of players registered, each player
    has maximum one bye. Players with the least number of wins are given preference
    for byes (this is ensured by cycling list backwardds).

    If no player is available who can be awarded a bye (mathematically implausible), function 
    will automatically return the player in last position.

    Returns:
      id: the unique id of the player who should be awarded a bye.
    """
    DB = connect()
    cursor = DB.cursor()
    standings = playerStandings()
    cursor.execute("SELECT player_id FROM players WHERE bye = FALSE; ")
    byes = cursor.fetchall()
    for j in range(1, countPlayers() + 1):
        id = standings[-j][0]
        for row in byes:
            if row[0] == id:
                print row[0]
                cursor.execute(
                    "INSERT INTO matches (winner_id,loser_id) VALUES (%s, %s) ;", (id, 0, ))
                print "hi"
                cursor.execute(
                    "UPDATE players SET bye = TRUE WHERE player_id = (%s);", (id,))
                DB.commit()
                cursor.close()
                DB.close()
                return id
    return standings[-1][0]


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []
    standings = playerStandings()
    count = countPlayers()

    if count % 2 != 0:
        bye_ID = checkAndSubmitBye()
        for i in range(count):
            if standings[i][0] == bye_ID:
                del standings[i]
                count -= 1

    for i in range(count):
        if i % 2 == 0:
            pairing = (standings[i][0], standings[i][1],
                       standings[i + 1][0], standings[i + 1][1])
            pairings.append(pairing)

    return pairings
