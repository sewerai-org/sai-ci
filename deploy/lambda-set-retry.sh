#!/bin/bash

ENV='';
if [ "${CIRCLE_BRANCH}" = "master" ]; then ENV='prod'; fi
if [ "${CIRCLE_BRANCH}" = "develop" ]; then ENV='dev'; fi

for service in "cort-${ENV}-api" "cort-${ENV}-tasker" "cort-${ENV}-worker"
do
    aws lambda put-function-event-invoke-config \
        --function-name $service \
        --maximum-retry-attempts 0 \
        --region us-west-2
done
