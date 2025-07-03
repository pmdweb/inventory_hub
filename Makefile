.PHONY: format lint test check

format:
	black .
	isort .

lint:
	flake8 .

test:
	pytest -v --cov --cov-report=term-missing

check: format lint test
