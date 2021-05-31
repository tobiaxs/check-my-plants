.PHONY: test
## Run pytest with codecov
test:
	pytest tests -vv --cov="." --cov-report=term --cov-report html --cov-fail-under=99 -p no:cacheprovider

.PHONY: lint
## Run black, isort and flake
lint:
	black . && isort . && flake8 .

.PHONY: schema
## Generate tortoise schema
schema:
	python src/database/migrate.py