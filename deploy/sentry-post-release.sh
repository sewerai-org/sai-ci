#!/bin/bash

# Assumes you're in a git repository and have the required env vars;
#    SENTRY_AUTH_TOKEN
#    SENTRY_ORG
VERSION=$(sentry-cli releases propose-version) 

if [ "${CIRCLE_BRANCH}" = "master" ]; then sentry-cli releases deploys $VERSION new -e prod; fi
if [ "${CIRCLE_BRANCH}" = "develop" ]; then sentry-cli releases deploys $VERSION new -e dev; fi
