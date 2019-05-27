EVOtz_webapp
============
EVOtz_webapp is a demo app for the EVO Summer Lab.

Main task was to build app to store and share files.

You can find deployed app `here
<http://evotz.herokuapp.com/>`_.

You can use credentials for user 'test' with pass '123' to test app without registration.

App capabilities
----------------

- Upload files to server.

- Share your uploaded files with anyone.

- Sign In to keep track of your files and get access to interesting features.

- Set date for your files to expire.

- !Warning! Due to being demo app you could upload files only up to 25 MB.

- !Warning! Server time is UTC+0.

- !Warning! Use http instead of https for custom CSS to load :(

Technologies used
-----------------

- Web framework : Pyramid

- Database : MongoDB

- Deploy : Heroku

Installing and Running locally
------------------------------

Python 3.6, Pyramid 1.10 and MongoDB 3.6 are required.

For Windows:
 - git clone https://github.com/dilex42/evotz_web.git

 - cd evotz_web

 - set VENV={{path_to_evotz_web}}\\env  (For ex. d:\\projects\\evotz_web\\env)

 - python -m venv %VENV%

 - %VENV%\\Scripts\\python setup.py develop

 - %VENV%\\Scripts\\python runapp.py

For Linux :
 - git clone https://github.com/dilex42/evotz_web.git

 - cd evotz_web

 - export VENV={{path_to_evotz_web}}/env  (For ex. home/projects/evotz_web/env)

 - python3 -m venv $VENV

 - $VENV/bin/python setup.py develop

 - $VENV/bin/python runapp.py

MongoDB setup :

  You need to install MongoDB and create an Instance. See detailed `official manual
  <https://docs.mongodb.com/manual/>`_.

  Then you need to set MONGODB_URI environmental variable to mongodb://MONGODB_USER:MONGODB_PASSWD@MONGODB_HOST:port/MONGODB_NAME

  Examples :

   - Windows : set MONGODB_URI=mongodb://me:123456@localhost:59806/my_db

   - Linux : export MONGODB_URI=mongodb://heroku_sada223:23fsddgs4sdfds@ds23576.mlab.com:59806/heroku_sada223

Tests
-----

Tests not working yet.
