#!/bin/bash

git pull --recurse-submodules
docker compose pull
docker compose up -d
docker image prune -f