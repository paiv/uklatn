.PHONY: all
.PHONY: build
.PHONY: test
.PHONY: clean

PYTHON ?= python

EXT_SUFFIX=$(shell $(PYTHON) -c 'import sysconfig; print(sysconfig.get_config_var("EXT_SUFFIX"))')
EXT_SOURCES=$(shell find . -name '*.c')
EXTENSIONS=$(EXT_SOURCES:%.c=%$(EXT_SUFFIX))

all: build

build: $(EXTENSIONS)

$(EXTENSIONS): $(EXT_SOURCES)
	@cd .. && $(PYTHON) setup.py build_ext --inplace

test: build
	@$(PYTHON) -m unittest discover -v -p '*_test.py'

clean:
	@cd .. && $(PYTHON) setup.py clean
	@find . -name '*.pyc' | xargs rm -v
	@find . -name '*.so' | xargs rm -v
	@find ../build -type d -name '__pycache__' | xargs rm -v -r
	@find .. -type d -name '*.egg-info' | xargs rm -v -r

