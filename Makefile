install:
	poetry install

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-uninstall-hc:
	pip uninstall hexlet-code
	rm -r dist

start_debug:
	python manage.py runserver

start:
	gunicorn task_manager.wsgi:application

lint:
	poetry run flake8 page_analyzer

pytest:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

build:
	./build.sh