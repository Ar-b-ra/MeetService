venv:
	rm -rf .venv/
	python3 -m venv .venv
	. .venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements/requirements.txt

venv_dev: venv
	. .venv/bin/activate && pip install -r requirements/requirements_dev.txt

test:
	. .venv/bin/activate && \
	coverage run --data-file tests/.coverage -m pytest -s && \
	coverage json --data-file tests/.coverage -o buf/tests/coverage.json && \
	coverage report --data-file tests/.coverage

lint:
	. .venv/bin/activate && \
	ruff check ./