venv:
	rm -rf .venv/
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements/requirements.txt

venv_dev: venv
	. .venv/bin/activate && pip install -r requirements/requirements_dev.txt

test:
	coverage run --data-file tests/.coverage -m pytest -s
	coverage json --data-file tests/.coverage -o buf/tests/coverage.json
	coverage report --data-file tests/.coverage

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics