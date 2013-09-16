develop:
	python setup.py develop

upload:
	python setup.py sdist upload develop

readme:
	pandoc --from=markdown --to=rst --output=README.rst README.md

tag:
	perl -p -i -e '/\d+\.\d+\.(\d+)/; my $x = $1+1; s/(\d+\.\d+\.)(\d+)/$1.$x/ge' sc/__init__.py
	git commit -m v`python setup.py --version` -a
	git tag -a v`python setup.py --version` -m v`python setup.py --version`
