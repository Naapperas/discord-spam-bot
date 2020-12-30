#!/bin/bash
ARG="Updated bot!"
if [ ! -z "$1" ]; then
    ARG="$1"
fi

RED='\033[0;31m'
NC='\033[0m'

echo "${RED} Your Github token is: c223a95bf811b9ddf9d2c42d945d52a1fcfac62b ${NC}"

bash ./heroku_deploy.sh "$ARG"
bash ./github_deploy.sh "$ARG"
