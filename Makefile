install:
	poetry install

start_debug:
	poetry run python manage.py runserver

start:
	gunicorn task_manager.wsgi:application

test:
	coverage run --source='.' manage.py test

lint:
	poetry run flake8 task_manager

test-coverage:
	coverage xml -o coverage.xml

show-test-coverage:
	coverage report

build:
	./build.sh
