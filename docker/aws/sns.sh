#!/usr/bin/env bash

aws --endpoint-url=http://localhost:4566 sns create-topic \
    --name $SNS_TOPIC \
    --region us-east-1