#!/usr/bin/env bash
    # --zip-file fileb://aws/function.zip \

aws lambda create-function \
    --endpoint-url=http://localhost:4566 \
    --function-name $LAMBDA_NAME \
    --runtime python3.10 \
    --handler lambda_function.lambda_handler \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --zip-file fileb:///etc/assets/function.zip \
    --region us-east-1