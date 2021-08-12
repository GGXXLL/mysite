# init db
.PHONY: init
init:
	python manage.py makemigrations
	python manage.py migrate


# start server
.PHONY: server
server:
	python manage.py runserver