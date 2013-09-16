develop:
	python setup.py develop

upload:
	python setup.py sdist upload develop

readme:
	pandoc --from=markdown --to=rst --output=README.rst README.md

