install:
	poetry install

start_debug:
	python manage.py runserver

start:
	gunicorn task_manager.wsgi:application

test:
	python manage.py test

lint:
	poetry run flake8 task_manager

# pytest:
# 	poetry run pytest

# test-coverage:
# 	poetry run pytest --cov=task_manager --cov-report xml

build:
	./build.sh