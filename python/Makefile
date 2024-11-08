.PHONY: all
.PHONY: test
.PHONY: clean

PYTHON ?= python

all: test

test:
	@$(PYTHON) -m unittest discover -v -p '*_tests.py'

clean:
	@find . -name '*.pyc' | xargs rm -v
	@find . -type d -name '__pycache__' | xargs rm -v -r
	@find . -type d -name '*.egg-info' | xargs rm -v -r

