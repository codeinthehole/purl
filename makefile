install:
	pip install -r requirements.txt
	python setup.py develop

test:
	nosetests

package: clean
	# Test these packages in a fresh virtualenvs:
	# $ pip install --no-index dist/purl-0.8.tar.gz
	# $ pip install --use-wheel --no-index --find-links dist purl
	./setup.py sdist
	./setup.py bdist_wheel

clean:
	-rm -rf dist/ build/
