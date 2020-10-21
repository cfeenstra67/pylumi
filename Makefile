

build-go:
	@mkdir -p build/go
	@cd go &&\
	go build -o ../build/go/libpylumigo.so -buildmode=c-shared connector/main.go
	@install_name_tool -id @rpath/libpylumigo.so build/go/libpylumigo.so


build: clean
	python setup.py bdist_wheel

install: clean
	python setup.py install

clean:
	@pip uninstall -y pylumi
	@rm -rf build/ dist/ *.egg-info .eggs
