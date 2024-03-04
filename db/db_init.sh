#!/bin/bash

echo "=== $BASH_SOURCE on $(hostname -f) at $(date)" >&2

echo start postgres
sudo /etc/init.d/postgresql start


sudo su - postgres -c \
"psql <<__END__

SELECT 'create the same user' ;
    CREATE USER $PG_USER ;
    ALTER USER $PG_USER CREATEDB;

SELECT 'grant him the priviledges' ;
    grant all privileges on database postgres to $PG_USER ;
    alter user postgres password '$PG_PW';

SELECT 'AND VERIFY' ;
    select * from information_schema.role_table_grants
    where grantee='""$PG_USER""' ;

SELECT 'INSTALL EXTENSIONS' ;
    CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";
    CREATE EXTENSION IF NOT EXISTS \"pgcrypto\";
    CREATE EXTENSION IF NOT EXISTS \"dblink\";

__END__
"
