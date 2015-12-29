-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- psql command to connect database
\c tournament 


-- Create table players to hold player names and player ids.
CREATE TABLE players (
	PRIMARY KEY (player_id),
	player_id 	SERIAL,
	name 		TEXT,
);


-- Create table matches to hold match ids, winning player's id and loser's id.
-- Loser_id is not a foreign key to accommodate for byes which are given automatic serial .
CREATE TABLE matches (
	PRIMARY KEY (match_id),
	match_id 	SERIAL,
	winner_id 	INTEGER REFERENCES players(player_id),
	loser_id 	INTEGER
);

-- Create a view to aggregate wins.
CREATE VIEW wins AS
	SELECT 	players.player_id, players.name, count(winner_id) AS number_wins
		FROM players LEFT JOIN matches
		ON players.player_id = matches.winner_id
		GROUP BY players.player_id;

-- Create a view to aggregate matches.
CREATE VIEW count_matches AS
	SELECT 	players.player_id, players.name, count(match_id) AS number_matches
		FROM players LEFT JOIN matches
		ON players.player_id = matches.winner_id
			OR players.player_id = matches.loser_id
		GROUP BY players.player_id;
