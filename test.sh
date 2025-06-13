#!/bin/bash

cd cluster-state
sudo docker build --progress=plain --no-cache -t kubegraph-cluster-state:latest .
cd ..

sudo docker compose -f docker-compose.test.yaml up
