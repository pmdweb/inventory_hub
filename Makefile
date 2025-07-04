.PHONY: format lint test check types clean help verify-coverage

format:
	black .
	isort .

lint:
	flake8 .

clean:
	rm -f .coverage*
	rm -rf htmlcov coverage.xml

test: clean
	pytest -v --cov --cov-report=term-missing --cov-report=xml

types:
	mypy .

check: format lint test types

verify-coverage:
	@if [ ! -f coverage.xml ]; then \
		echo "❌ coverage.xml not found. Did you run 'make test'?"; \
		exit 1; \
	else \
		echo "✅ coverage.xml found."; \
	fi

help:
	@echo "Available targets:"
	@echo "  format            - Format code using Black and isort"
	@echo "  lint              - Run flake8 linter"
	@echo "  clean             - Remove coverage and htmlcov artifacts"
	@echo "  test              - Run tests with coverage"
	@echo "  types             - Run mypy static type checks"
	@echo "  check             - Run all checks (format, lint, test, types)"
	@echo "  verify-coverage   - Check if coverage.xml exists"
