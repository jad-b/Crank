reqs:
	pip install -U -r requirements.txt

test: unit

unit:
	nosetests --with-coverage crank/*

lint:
	flake8 $(shell find . -name '*.py' -type f)

clean:
	find . -name '*.orig' -o -name '*.swp' -delete
