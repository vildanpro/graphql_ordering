VERSION = 1.8

.DEFAULT_GOAL = version
.PHONY: version
version:
	@ echo "Script version:" $(VERSION)


.PHONY: run
run:  
	@ /usr/bin/env python manage.py runserver

.PHONY: serve
serve:
	@ gunicorn -c .gunicorn.py manage:app


.PHONY: requirements
requirements: ENV="production"
requirements:
	@ /usr/bin/env python setup.py requirements -e ${ENV}

.PHONY: lint
lint:
	@ flake8

.PHONY: coverage
coverage: ARGS = "-x"
coverage: 
	@ rm -rf htmlcov
	@ py.test tests --cov ${ARGS}

.PHONY: test
test: ARGS = "-vx"
test: 
	@ py.test tests ${ARGS}


.PHONY: clean
clean:  
	@ find . -name "*.pyc" -delete
	@ find . -name "*.orig" -delete


.PHONY: shell
shell: 
	@ /bin/sh

.PHONY: python
python: 
	@ /usr/bin/env python
