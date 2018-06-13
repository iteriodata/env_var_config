.PHONY: test update_dependencies clean build release_to_test_pypi release_to_pypi 

test:
	tox

update_dependencies:
	.tox/py36/bin/pip-compile requirements-test.in
	tox -r

clean:
	-rm -rf build dist *.egg-info

build: clean
	.tox/py36/bin/python setup.py sdist bdist_wheel

release_to_test_pypi: build
	.tox/py36/bin/twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release_to_pypi: build
	.tox/py36/bin/twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
