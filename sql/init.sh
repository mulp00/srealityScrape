#!/bin/bash

psql -U $POSTGRES_USER -d $POSTGRES_DB -a -f /proj01/scripts/db/init.sql
