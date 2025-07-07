.PHONY: format lint test check types clean help verify-coverage htmlcov

# 🔷 Formata código com Black + isort
format:
	black .
	isort .

# 🔷 Lint com flake8
lint:
	flake8 .

# 🔷 Remove artefatos antigos
clean:
	rm -f .coverage*
	rm -rf htmlcov coverage.xml

# 🔷 Executa testes com cobertura
test: clean
	pytest -v \
		--cov \
		--cov-config=.coveragerc \
		--cov-report=term-missing \
		--cov-report=xml

# 🔷 Executa análise estática de tipos com mypy
types:
	mypy .

# 🔷 Executa todos os checks
check: format lint test types

# 🔷 Verifica se coverage.xml foi gerado
verify-coverage:
	@if [ ! -f coverage.xml ]; then \
		echo "❌ coverage.xml not found. Did you run 'make test'?"; \
		exit 1; \
	else \
		echo "✅ coverage.xml found."; \
	fi

# 🔷 Gera relatório HTML da cobertura
htmlcov: test
	@echo "Generating HTML coverage report..."
	coverage html -d htmlcov
	@echo "Open htmlcov/index.html in your browser."

# 🔷 Ajuda
help:
	@echo "Available targets:"
	@echo "  format            - Format code using Black and isort"
	@echo "  lint              - Run flake8 linter"
	@echo "  clean             - Remove coverage and htmlcov artifacts"
	@echo "  test              - Run tests with coverage"
	@echo "  htmlcov           - Generate HTML coverage report"
	@echo "  types             - Run mypy static type checks"
	@echo "  check             - Run all checks (format, lint, test, types)"
	@echo "  verify-coverage   - Check if coverage.xml exists"
