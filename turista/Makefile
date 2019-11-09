CWD=$(shell pwd)
PKG=turista

clean:
	find ./$(PKG) -name "*.pyc" -exec rm -rfv {} \;

test:
	tox -r

.PHONY: test clean
