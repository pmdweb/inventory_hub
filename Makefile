.PHONY: format lint test check types clean

format:
	black .
	isort .

lint:
	flake8 .

clean:
	rm -f .coverage*
	rm -rf htmlcov

test: clean
	pytest -v --cov --cov-report=term-missing

types:
	mypy .

check: format lint test
