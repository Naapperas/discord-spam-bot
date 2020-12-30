#!/bin/bash
ARG="Updated bot!"
if [ ! -z "$1" ]; then
    ARG=$1
fi
bash ./heroku_deploy.sh $ARG
bash ./github_deploy.sh $ARG
