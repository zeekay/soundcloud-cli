develop:
	python setup.py develop

upload:
	python setup.py sdist upload develop

readme:
	pandoc --from=markdown --to=rst --output=README.rst README.md

tag:
	git commit -m v`python setup.py --version` -a
	git tag -a v`python setup.py --version` -m v`python setup.py --version`
