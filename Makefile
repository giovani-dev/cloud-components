lambdaName = base-lambda
pythonVersion = python3.10
handler = lambda_function.lambda_handler
package = src

run_docker:
	docker-compose -f ./docker/docker-compose.yml up --build -d

stop_docker:
	docker-compose -f ./docker/docker-compose.yml stop

create_lambda:
	aws --endpoint-url=http://localhost:4566 lambda create-function \
		--function-name $(lambdaName) \
		--runtime $(pythonVersion) \
		--handler $(handler) \
		--memory-size 128 \
		--architectures arm64 \
		--timeout 3600 \
		--zip-file fileb://build/deployment_package.zip \
		--role arn:aws:iam::111111111111:role/apigw \
		--environment Variables={}

deploy_in_lambda:
	aws --endpoint-url=http://localhost:4566 lambda update-function-code \
		--function-name $(lambdaName) \
		--zip-file fileb://build/deployment_package.zip

run_lambda:
	if [ ! -d ./docker/out ] ; then mkdir ./docker/out ; fi
	aws --endpoint-url=http://localhost:4566 lambda invoke \
		--payload file://mock/event.json \
		--function-name $(lambdaName) \
		--log-type Tail \
		--query 'Payload' \
		--output json \
		--cli-binary-format raw-in-base64-out ./docker/out/$(lambdaName).json

build_src:
	if [ ! -d ./build ] ; then mkdir ./build ; fi
	rm -rf ./build/src
	mkdir ./build/src
	poetry export -f requirements.txt --output ./build/src/requirements.txt --without-hashes
	pip install \
		--platform manylinux2014_aarch64 \
		--target=$(lambdaName) \
		--implementation cp \
		--python 3.10 \
		--only-binary=:all: \
		--upgrade \
		-r ./build/src/requirements.txt -t ./build/src
	cp -r ./$(package) ./build/src/$(package)
	cp ./$(package)/interface/lambda_function.py ./build/src/lambda_function.py
	cd ./build/src ; zip -r9 ../deployment_package.zip .

