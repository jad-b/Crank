reqs:
	pip install -U -r requirements.txt

unit: 
	nosetests crank/*

lint: 
	pep8 crank/*
	pyflakes crank/*

clean:
	find . -name '*.orig' -delete
	find . -name '*.swp' -delete
