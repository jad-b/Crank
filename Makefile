reqs:
	pip install -U -r requirements.txt

unit: 
	nosetests --with-coverage crank/*

lint: 
	pep8 crank/*
	pyflakes crank/*

clean:
	find . -name '*.orig' -delete
	find . -name '*.swp' -delete
