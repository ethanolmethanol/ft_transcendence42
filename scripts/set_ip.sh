#!/bin/bash

get_ip() {
    if [ "$1" == "prod" ]; then
        hostname -i | awk '{print $1}'
    else
        echo -n "localhost"
    fi
}

create_nginx_config_file() {

    local serv_ip
    local nginx_config_template
    local nginx_config_file

	serv_ip=$(get_ip "$1")
	nginx_config_template="front/nginx/nginx.conf.template"
    nginx_config_file="front/nginx/nginx.conf"

    if [ -f "$nginx_config_template" ]; then
        sed "s/\${SERV_IP}/$serv_ip/g" "$nginx_config_template" > "$nginx_config_file"
    else
        echo "Nginx config template file not found"
        exit 1
    fi
}

update_environment_ts() {

    local serv_ip
    local env_file
    local env_file_template

	serv_ip=$(get_ip $1)
	env_file="front/src/environments/environment.ts"
	env_file_template="front/src/environments/environment.template.ts"

    if [ -f "$env_file_template" ]; then
    	sed "s/\${SERV_IP}/$serv_ip/g" "$env_file_template" > "$env_file"
    else
        echo "environment.template.ts file not found"
        exit 1
    fi
}

create_nginx_config_file $1
update_environment_ts $1
