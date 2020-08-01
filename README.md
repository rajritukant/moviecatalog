# moviecatalog
Creates a movie catalog where users can create collections and add movies to them

## Steps to run

* make virtual env
* run migrations
* create superuser with below credentials
	username: admin
	password: password
* add client id and secret to myproject/moviecoll/config.py

* use the same to login and obtain a token


Note: right now users are registered using django admin
and then their credentials used to obtain jwt token.


and then hit apis
sharing postman collection also
