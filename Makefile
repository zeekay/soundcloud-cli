develop:
	python setup.py develop

upload:
	python setup.py sdist upload develop

readme:
	pandoc --from=markdown --to=rst --output=README.rst README.md

tag:
	perl -p -i -e '/\d+\.\d+\.(\d+)/; my $$x = $$1+1; s/(\d+\.\d+\.)(\d+)/$$1.$$x/ge' soundcloud_cli/__init__.py
	export version=`python setup.py --version`; \
		git ci -m v$$version -a; \
		git tag -a v$$version -m v$$version

.PHONY: develop upload readme tag
