FROM postgres:15 as db
WORKDIR /proj01
COPY ./sql/init.sh /docker-entrypoint-initdb.d
COPY ./sql/init.sql ./scripts/db/init.sql