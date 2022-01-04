

PULUMI_VERSION:=3.21.0

PART:=patch

build: clean
	python setup.py sdist bdist_wheel
	setuptools-golang-build-manylinux-wheels

install: clean
	python setup.py install

pypi-check:
	twine check dist/*

pypi-upload-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

update-pulumi-version:
	@bumpversion \
		--config-file .bumpversion-pulumi.cfg \
		--new-version $(PULUMI_VERSION) \
		--allow-dirty \
		--list major

bumpversion:
	@bumpversion --list $(PART)

pypi-upload:
	twine upload dist/*

clean:
	@pip uninstall -y pylumi
	@rm -rf build/ dist/ *.egg-info .eggs

test:
	py.test -vv tests

fmt:
	black pylumi setup.py docs/conf.py tests

check-fmt:
	black pylumi setup.py docs/conf.py tests --check
