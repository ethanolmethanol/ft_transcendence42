NAME			= ft_transcendence

DATADIRS		= db/data/ front/dist/transcendence/browser/ ~/tr_certs

ENV_SRC			= ~/.env

ENV_FILE		= .env

# WIP
# DB_NAME		= $$(grep POSTGRES_DB ${ENV_FILE} | sed "s.POSTGRES_DB='(.*)'.\1.")

BROWSER			= firefox

SHELL			= /bin/bash

CONTAINERS		= db back_auth front prometheus grafana node_exporter blackbox_exporter # pong redis

COMPOSE_PATH	= docker-compose.yml

COMPOSE			= docker compose -f ${COMPOSE_PATH}

R				= \033[1;31m # RED
G				= \033[1;32m # GREEN
Y				= \033[1;33m # YELLOW
C				= \033[1;34m # CYAN
M				= \033[1;35m # MAGENTA
N				= \033[0m    # RESET

# Mkcert installation
MKCERT_VERSION	= v1.4.3
MKCERT_BIN		= mkcert
MKCERT_URL		= https://github.com/FiloSottile/mkcert/releases/download/$(MKCERT_VERSION)/mkcert-$(MKCERT_VERSION)-linux-amd64
CERT_DIR 		= ssl/
CERT_PATH 		= $(CERT_DIR)/serv.crt
KEY_PATH 		= $(CERT_DIR)/serv.key
LOCAL_BIN		= $(HOME)/bin
SSL_CONT_DIRS	= front/ssl back_auth/ssl
SSL_DIRS		= $(LOCAL_BIN)/$(MKCERT_BIN) $(CERT_DIR) $(SSL_CONT_DIRS)

# Architecture
UNAME			= $(shell uname)

${NAME}: gen-cert up health
	$(call printname)

# ${ENV_FILE}

up: | ${DATADIRS} ${ENV_FILE}
	@echo "Up-ing containers:"
	${COMPOSE} up -d --build

${DATADIRS}:
	mkdir -p ${DATADIRS}

down:
	@echo "Down-ing containers:"
	${COMPOSE} down

all: ${NAME}

${ENV_FILE}:
	@if test -f ${ENV_SRC} && cp ${ENV_SRC} $@; then echo -e "$GFetched environment file [$C.env$G] from ..$N"; \
	else echo -e "$RPlease make an environment file [$C.env$R] using .env_template file$N"; \
	exit 1; fi

######## INFO / DEBUGGING / TROUBLESHOOTING ########

# WIP
# hellodb:
# 	echo $(DB_NAME)

testform:
	python3 -m http.server -d back_auth/test_form -b localhost 1234

health:
	while docker ps | grep "health: starting" > /dev/null; do true; done
	if [ $$(docker ps | grep -c "(healthy)") -eq $$(echo $(CONTAINERS) | wc -w) ]; then \
		echo -e "$(G)All is good :)$(N)"; \
		exit 0; \
	else \
		echo -e "$(R)Something's wrong... :/$(N)"; \
		docker ps -a | grep -v "(healthy)"; \
		exit 1; \
	fi \

info:
	@docker ps -a

infor:
	@while true; do clear; docker ps -a; sleep 5s; done

logs:
	@for cont in ${CONTAINERS}; \
	do echo "Logs for $$cont:"; docker logs $$cont; done

wlogs:
	@PS3="Select which container's logs you want: "; \
	select c in ${CONTAINERS}; \
	do echo "Logs for $$c:"; docker logs $$c; exit $?; done

logsize:
	sudo sh -c "du -ch /var/lib/docker/containers/*/*-json.log"

rmlogs:
	sh -c "truncate -s 0 /var/lib/docker/containers/**/*-json.log"

restart:
	sudo service docker restart

talk:
	@PS3="Select for which container you want to access a shell: "; \
	select c in ${CONTAINERS}; \
	do echo "Shell for $$c:"; docker exec -it $$c ${SHELL}; exit $?; done

rmi:
	@PS3="Select for which image you want to remove: "; \
	select c in ${CONTAINERS}; \
	do echo "Downing and deleting image $$c:"; docker-compose down $$c && docker rmi $$c; exit $?; done

nginxlogs:
	@docker exec -it nginx cat /var/log/nginx/error.log

dbip:
	@docker exec -it db hostname -i

fix:
	sudo chmod 666 /var/run/docker.sock

dev: all
	cd front/; npm run watch

install-mkcert:
	@if [ $(UNAME) = "Darwin" ]; then \
		echo "Checking for mkcert installation..."; \
		if ! command -v mkcert &>/dev/null; then \
			echo "mkcert not found, installing..."; \
			brew install mkcert; \
		else \
			echo "mkcert is already installed."; \
		fi; \
	else \
		if [ ! -e "$(LOCAL_BIN)/$(MKCERT_BIN)" ]; then \
			echo "Downloading mkcert..."; \
			mkdir -p $(LOCAL_BIN); \
			curl -L $(MKCERT_URL) -o $(MKCERT_BIN); \
			chmod +x $(MKCERT_BIN); \
			mv $(MKCERT_BIN) $(LOCAL_BIN); \
		fi; \
		export PATH="$(LOCAL_BIN):$$PATH"; \
	fi
	@mkcert -version

gen-cert: install-mkcert
	@if [ ! -e "$(CERT_DIR)" ]; then \
		mkcert serv localhost 127.0.0.1 ::1; \
		mkdir -p $(CERT_DIR); \
		mv ./serv+3.pem $(CERT_PATH); \
		mv ./serv+3-key.pem ./$(KEY_PATH); \
	fi
	for dir in $(SSL_CONT_DIRS); do \
		mkdir -p $$dir; \
		cp -r $(CERT_DIR) $$dir; \
	done; \

clean:
	@${COMPOSE} down -v

fclean: clean
	@docker --log-level=warn system prune -f
	@for dir in $(SSL_DIRS); do \
		if [ -d "$$dir" ]; then \
			rm -rf $$dir; \
		fi; \
	done

ffclean: fclean
	@docker --log-level=warn system prune -af
	@ rm -rf ${DATADIRS}
	@echo -e "$CDeleted data directories [$Y${DATADIRS}$C]$N"

re: fclean all

######## FUNKY STUFF ########

.PHONY: fclean full all datadirs fix logs nginxlogs wlogs dbip info re talk clean down infor up health install-mkcert gen-cert
.SILENT: health
