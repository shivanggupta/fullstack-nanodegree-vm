# Book Catalog 

Book Catalog is a web application developed using the Flask framework in Python.Created for the [Udacity](http://www.udacity.com) Fullstack Nanodegree project 2 by Shivang Gupta, this version of Book Catalog is a work in progress.

In this application, there are various pre-defined Genres, and a User can add a Book to any Genre. Users can log in using Google Plus (third party authentication) and logged in users can edit/delete their own items. The application also provides a JSON API endpoint.

Images and User profile pages are a work in progress (You may find placeholders for these in some places)

To get started, check out the instructions below!


## Table of contents

* [Quick start](#quick-start)
* [Documentation](#documentation)
* [Creators](#creators)
* [Copyright and license](#copyright-and-license)


## Quick start

Use Terminal/PowerShell/cmd for the following:

* Access the vagrant machine inside the fullstack-nanodegree-vm repository and power up hte virtual machine.
* In the vagrant machine, use `ls` and `cd` to locate `catalog` subdirectory (The folder contains this README).
* In the `templates` directory locate the `login.html` file and in this file edit `line 58` with your google client ID. You can add the project to your Google account as `Book Listings App`
* Run `python database_setup.py` to set up the database. 
* Run `python somebooks.py` to populate the database. 
* Run `python application.py` to deploy the web server.
* Visit `localhost:8000/` on your favorite browser and navigate the app. (Tested in Google Chrome) 



Read the comments in the code for more information.

## Documentation

Within the repository you'll find the following directories and files:

```
fullstack-nanodegree-vm
  -vagrant
      └── catalog
        ├── application.py
        ├── database_setup.py
        ├── somebooks.py
        └── README.md
        └── templates
	        ├── books.html
	        ├── genres.html
	        ├── newbook.html
	        ├── editbook.html
	        ├── login.html
	        ├── allbooks.html
	        ├── about.html
	        └── deletebook.html
	    └── static
	        ├── shop-homepage.css
	        ├── bootstrap.min.cs
	        ├── boostrap.min.js
	        └── jquery.js
```


## Creators

**Shivang Gupta**




## Copyright and license

Code released under [the MIT license](https://github.com/twbs/bootstrap/blob/master/LICENSE).
Docs released under [Creative Commons](https://github.com/twbs/bootstrap/blob/master/docs/LICENSE).
