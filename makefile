install:
	pip install -r requirements.txt
	python setup.py develop

test:
	nosetests
