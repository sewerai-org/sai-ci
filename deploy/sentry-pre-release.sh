#!/bin/bash

# Assumes you're in a git repository and have the required env vars;
#    SENTRY_AUTH_TOKEN
#    SENTRY_ORG
VERSION=$(sentry-cli releases propose-version) 

# Create a release
sentry-cli releases new -p cortland $VERSION

# Associate commits with the release
sentry-cli releases set-commits --auto $VERSION