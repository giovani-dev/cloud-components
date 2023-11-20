#!/usr/bin/env bash

aws sqs create-queue \
    --endpoint-url=http://localhost:4566 \
    --queue-name $QUEUE_NAME \
    --region us-east-1