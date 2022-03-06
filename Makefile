PYTHON = python3
PYTHON_FILES := $(shell find . -name "*.py" -not -path "./docs*")

.PHONY = format check test

format:
	black $(PYTHON_FILES)

check:	
	black --check --verbose $(PYTHON_FILES)
	mypy $(PYTHON_FILES)
	pylint $(PYTHON_FILES)

test:
	python -m pytest