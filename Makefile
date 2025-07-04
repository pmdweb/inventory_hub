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
	pytest -v --cov --cov-report=term-missing --cov-report=xml

types:
	mypy .

check: format lint test types

# Show help
help:
	@echo "Available targets:"
	@echo "  format   - Format code using Black and isort"
	@echo "  lint     - Run flake8 linter"
	@echo "  clean    - Remove coverage and htmlcov artifacts"
	@echo "  test     - Run tests with coverage"
	@echo "  types    - Run mypy static type checks"
	@echo "  check    - Run all checks (format, lint, test, types)"
