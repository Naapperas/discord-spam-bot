#!/bin/bash
ARG="Updated bot!"
if [ ! -z "$1" ]; then
    ARG="$1"
fi

RED='\033[0;31m'
NC='\033[0m'

#bash ./heroku_deploy.sh "$ARG"

echo -e "${RED}Your token is: $TOKEN ${NC}"

bash ./github_deploy.sh "$ARG"
