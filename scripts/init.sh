#!/bin/bash

get_ip() {
	if [ "$1" == "prod" ]; then
		ip=$(hostname -i 2>/dev/null) || ip=$(ifconfig | awk '/inet / && !/127.0.0.1/ {print $2}' | head -n 1)
		echo "$ip"
	else
		echo -n "localhost"
	fi
}

clean_up() {
	rm -rf "${CERT_DIR}" "${SSL_CONT_DIRS[@]}" "${ENV_FILE_FRONT}" "${NGINX_CONFIG_FILE}" "${ENV_FILE_GLOBAL}"
	exit 0
}

prompt_for_env() {
	if [ -f "${ENV_FILE_GLOBAL}" ]; then
		echo "Found .env file"
		return
	fi

	[ -z "${POSTGRES_USER}" ] && read -rp "Enter PostgreSQL User: " POSTGRES_USER
	[ -z "${POSTGRES_PASSWORD}" ] && read -rsp "Enter PostgreSQL Password: " POSTGRES_PASSWORD && echo
	[ -z "${POSTGRES_DB}" ] && read -rp "Enter PostgreSQL Database Name: " POSTGRES_DB
	[ -z "${OAUTH_CLIENT_UID}" ] && read -rp "Enter OAuth Client UID: " OAUTH_CLIENT_UID
	[ -z "${OAUTH_CLIENT_SECRET}" ] && read -rsp "Enter OAuth Client Secret: " OAUTH_CLIENT_SECRET && echo
	[ -z "${MINIO_ROOT_USER}" ] && read -rp "Enter Minio Root User: " MINIO_ROOT_USER
	[ -z "${MINIO_ROOT_PASSWORD}" ] && read -rsp "Enter Minio Root Password: " MINIO_ROOT_PASSWORD && echo

	echo "POSTGRES_USER='${POSTGRES_USER}'" >"${ENV_FILE_GLOBAL}"
	{
		echo "POSTGRES_PASSWORD='${POSTGRES_PASSWORD}'"
		echo "POSTGRES_DB='${POSTGRES_DB}'"
		echo "SERV_IP='${IP_ADDR}'"
		echo "OAUTH_CLIENT_UID='${OAUTH_CLIENT_UID}'"
		echo "OAUTH_CLIENT_SECRET='${OAUTH_CLIENT_SECRET}'"
		echo "MINIO_ROOT_USER='${MINIO_ROOT_USER}'"
		echo "MINIO_ROOT_PASSWORD='${MINIO_ROOT_PASSWORD}'"
	} >>"${ENV_FILE_GLOBAL}"

	echo "'${ENV_FILE_GLOBAL}' file created with the following content:"
	cat "${ENV_FILE_GLOBAL}"
}

generate_certificates() {
	if [ -e "${CERT_DIR}" ]; then
		echo "Found certificates files"
		return
	fi

	local key_path="${CERT_DIR}/private.key"
	local cert_path="${CERT_DIR}/public.crt"

	# generate certificates files
	mkcert serv "${IP_ADDR}" 127.0.0.1 ::1
	mkdir -p "${CERT_DIR}"
	mv ./serv+3.pem "${cert_path}"
	mv ./serv+3-key.pem "${key_path}"

	# distribute certificates
	for dir in "${SSL_CONT_DIRS[@]}"; do
		mkdir -p "$dir"
		cp -r "${CERT_DIR}" "$dir"
	done
}

create_nginx_config_file() {
	local nginx_config_template

	nginx_config_template="front/nginx/nginx.conf.template"

	if [ -f "$nginx_config_template" ]; then
		sed "s/\${SERV_IP}/$IP_ADDR/g" "$nginx_config_template" >"${NGINX_CONFIG_FILE}"
	else
		echo "Nginx config template file not found"
		exit 1
	fi
}

update_environment_ts() {
	local env_file_template_front

	env_file_template_front="front/src/environments/environment.template.ts"

	if [ -f "${env_file_template_front}" ]; then
		sed "s/\${SERV_IP}/$IP_ADDR/g" "${env_file_template_front}" >"${ENV_FILE_FRONT}"
	else
		echo "environment.template.ts file not found"
		exit 1
	fi
}

install_mkcert_for_mac() {
	echo "Checking for mkcert installation..."
	if ! command -v mkcert &>/dev/null; then
		echo "mkcert not found, installing..."
		brew install mkcert
	else
		echo "mkcert is already installed."
	fi
}

install_mkcert_for_linux_64() {
	local mkcert_version="v1.4.3"
	local mkcert_bin="mkcert"
	local mkcert_url="https://github.com/FiloSottile/mkcert/releases/download/${mkcert_version}/mkcert-${mkcert_version}-linux-amd64"
	local local_bin=${HOME}/bin

	if [ ! -e "${local_bin}/${mkcert_bin}" ]; then
		echo "Downloading mkcert..."
		mkdir -p "${local_bin}"
		curl -L "${mkcert_url}" -o "${mkcert_bin}"
		chmod +x "${mkcert_bin}"
		mv "${mkcert_bin}" "${local_bin}"
	fi

	export PATH="${local_bin}:$PATH"
}

install_mkcert() {
	if [ "$(uname)" = "Darwin" ]; then
		install_mkcert_for_mac
	else
		install_mkcert_for_linux_64
	fi
	mkcert -version
}

export_env_instructions() {
	echo -e "\n**************************** EXPORT ENV INSTRUCTIONS ****************************"
	echo "*  To apply the environment variables to your current shell, please run:        *"
	echo "*  [ZSH]    set -a; source ${ENV_FILE_GLOBAL}; set +a                                         *"
	echo "*  [BSH]    source ${ENV_FILE_GLOBAL}                                                         *"
	echo -e "*********************************************************************************\n"
}

IP_ADDR=$(get_ip "$1")
CERT_DIR="ssl/"
SSL_CONT_DIRS=(front/ssl back/ssl minio/ssl)
ENV_FILE_FRONT="front/src/environments/environment.ts"
NGINX_CONFIG_FILE="front/nginx/nginx.conf"
ENV_FILE_GLOBAL=".env"

if [ "$1" == "clean" ]; then
	clean_up
else
	prompt_for_env
	install_mkcert
	generate_certificates
	create_nginx_config_file
	update_environment_ts
	export_env_instructions
fi
