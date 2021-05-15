install:
	pip install -r requirements.txt
	flit install --symlink

test:
	pytest

package: clean
	flit build

release:
	flit publish
	git push --tags

clean:
	-rm -rf dist/ build/ *.egg-info
