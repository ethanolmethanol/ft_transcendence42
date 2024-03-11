NAME			= ft_transcendence

DATADIRS		= db/data/

ENV_SRC			= ~/.env

ENV_FILE		= .env

DOMAIN_NAME		= $$(grep DOMAIN ${ENV_FILE} | sed 's.DOMAIN_NAME=..')

BROWSER			= firefox

SHELL			= /bin/bash

CONTAINERS		= back_auth front db prometheus grafana node_exporter blackbox_exporter

COMPOSE_PATH	= docker-compose.yml

COMPOSE			= docker compose -f ${COMPOSE_PATH}

R				= \033[1;31m # RED
G				= \033[1;32m # GREEN
Y				= \033[1;33m # YELLOW
C				= \033[1;34m # CYAN
M				= \033[1;35m # MAGENTA
N				= \033[0m    # RESET

${NAME}: up
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

testform:
	python3 -m http.server -d back_auth/test_form -b localhost 1234

health:
	while docker ps | grep "health: starting" > /dev/null; do true; done
	if [ $$(docker ps | grep -c "healthy") -eq $$(echo $(CONTAINERS) | wc -w) ]; then \
		echo -e "$(G)All is good :)$(N)"; \
		exit 0; \
	else \
		echo -e "$(R)Something's wrong... :/$(N)"; \
		exit 1; \
	fi

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

nginxlogs:
	@docker exec -it nginx cat /var/log/nginx/error.log

dbip:
	@docker exec -it db hostname -i

fix:
	sudo chmod 666 /var/run/docker.sock

clean:
	@${COMPOSE} down -v

fclean: clean
	@docker --log-level=warn system prune -af

ffclean: fclean
	@sudo rm -rf ${DATADIRS}
	@echo -e "$CDeleted data directories [$Y${DATADIRS}$C]$N"

re: fclean all

######## FUNKY STUFF ########

.PHONY: fclean full all datadirs fix logs nginxlogs wlogs dbip info re talk clean down infor up health
.SILENT: health