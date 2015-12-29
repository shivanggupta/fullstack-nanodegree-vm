# Tournament Results

Tournament Results is a simple sql relational database project, designed to generate pairings for a swiss style tournament. Created for the [Udacity](http://www.udacity.com) Fullstack Nanodegree project 2 by Shivang Gupta, this version of Tournamnet Results is a work in progress.

To get started, check out the instructions below!


## Table of contents

* [Quick start](#quick-start)
* [Documentation](#documentation)
* [Creators](#creators)
* [Copyright and license](#copyright-and-license)


## Quick start


* Access the vagrant machine inside the fullstack-nanodegree-vm repository and power up hte virtual machine.
* In the vagrant machine, use `ls` and `cd` to locate `tournament` subdirectory (The folder contains this README).
* Run `psql` command and check if the tables are setup using `\dt`, else import the database with `\i tournament.sql`.
* Run `python tournament_test.py' to run the unit tests. 

Read the comments in the code for more information.

## Documentation

Within the repository you'll find the following directories and files:

```
fullstack-nanodegree-vm
  -vagrant
      └──tournament
        ├── tournament.py
        ├── tournament_test.py
        ├── tournament.sql
        └── README.md
```


## Creators

**Shivang Gupta**

* <shivanggupta6@gmail.com>



## Copyright and license

Code released under [the MIT license](https://github.com/twbs/bootstrap/blob/master/LICENSE).
Docs released under [Creative Commons](https://github.com/twbs/bootstrap/blob/master/docs/LICENSE).
