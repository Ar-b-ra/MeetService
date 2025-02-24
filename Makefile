venv:
	rm -rf .venv/
	python3 -m venv .venv
	.venv/bin/python3 -m pip install --upgrade pip
	.venv/bin/python3 -m pip install -r requirements/requirements.txt

venv_dev: venv
	.venv/bin/python3 -m pip install -r requirements/requirements_dev.txt

test:
	.venv/bin/python3 -m coverage run --data-file tests/.coverage -m pytest -s
	.venv/bin/python3 -m coverage json --data-file tests/.coverage -o buf/tests/coverage.json
	.venv/bin/python3 -m coverage report --data-file tests/.coverage

lint:
	.venv/bin/python3 -m ruff check ./
	
run:
	.venv/bin/python3 -m fastapi run app/app.py