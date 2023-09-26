bucket = qualquer-coisa

run_docker:
	docker-compose -f ./docker/docker-compose.yml up --build -d

stop_docker:
	docker-compose -f ./docker/docker-compose.yml stop

create_bucket:
	aws --endpoint-url=http://localhost:4566 s3api create-bucket --bucket $(bucket)

test:
	poetry run pytest -v

lint:
	poetry run pylint $(LINT_PATH)

install_pkg:
	pip install --upgrade pip
	pip install -U pip setuptools
	pip install poetry
	poetry install

install_poetry:
	pip install --upgrade pip
	pip install -U pip setuptools
	pip install poetry

build_src:
	poetry build

publish:
	poetry publish -u $(PYPI_USER) -p $(PYPI_PWD)