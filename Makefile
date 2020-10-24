

PULUMI_VERSION:=2.12.0

PART:=patch


build-go:
	@mkdir -p build/go
	@cd go &&\
	go build -o ../build/go/libpylumigo.so -buildmode=c-shared connector/main.go
	@install_name_tool -id @rpath/libpylumigo.so build/go/libpylumigo.so


build: clean
	python setup.py sdist bdist_wheel

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
