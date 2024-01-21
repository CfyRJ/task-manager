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

test:
	python manage.py test

lint:
	poetry run flake8 task_manager --exclude=settings.py

# pytest:
# 	poetry run pytest

# test-coverage:
# 	poetry run pytest --cov=task_manager --cov-report xml

build:
	./build.sh