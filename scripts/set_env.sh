#!/bin/bash

# Function to get the local IP address
get_ip() {
    if [ "$1" == "prod" ]; then
        hostname -i | awk '{print $1}'
    else
        echo -n "localhost"
    fi
}

# Function to prompt for user input if .env file does not exist
prompt_for_env() {
    read -p "Enter PostgreSQL User: " postgres_user
    read -sp "Enter PostgreSQL Password: " postgres_password
    echo
    read -p "Enter PostgreSQL Database Name: " postgres_db
    ip_address=$(get_ip $1)

    echo "POSTGRES_USER='$postgres_user'" > .env
    echo "POSTGRES_PASSWORD='$postgres_password'" >> .env
    echo "POSTGRES_DB='$postgres_db'" >> .env
    echo "SERV_IP='$ip_address'" >> .env

    echo ".env file created with the following content:"
    cat .env
}

if [ ! -f ".env" ]; then
    prompt_for_env $1
else
    echo "Found .env file"
fi
