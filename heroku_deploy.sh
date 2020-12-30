#!/bin/bash

git add .
git commit -am "$1"
git push heroku main
