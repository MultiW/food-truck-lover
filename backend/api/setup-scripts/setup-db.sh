#!/bin/bash

psql -f 'api/setup-scripts/create-db.sql'
python api/setup-scripts/seed_db.py