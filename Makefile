install:
	poetry install

start_debug:
	poetry run python manage.py runserver

start:
	gunicorn task_manager.wsgi:application

test:
	poetry run python manage.py test

lint:
	poetry run flake8 task_manager

# test-coverage:
# 	poetry run pytest --cov=task_manager --cov-report xml

build:
	./build.sh