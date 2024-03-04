NAME			= ft_transcendence

DATADIRS		= db/data/

ENV_SRC			= ~/.env

ENV_FILE		= .env

DOMAIN_NAME		= $$(grep DOMAIN ${ENV_FILE} | sed 's.DOMAIN_NAME=..')

BROWSER			= firefox

SHELL			= /bin/bash

CONTAINERS		= back front db

COMPOSE_PATH	= docker-compose.yml

COMPOSE			= docker compose -f ${COMPOSE_PATH}

R				= \e[31m# RED
G				= \e[32m# GREEN
Y				= \e[33m# YELLOW
C				= \e[34m# CYAN
M				= \e[35m# MAGENTA
N				= \e[0m#  RESET

${NAME}: up
	$(call printname)

# ${ENV_FILE}

up: | ${DATADIRS}
	@echo "Up-ing containers:"
	${COMPOSE} up -d --build

${DATADIRS}:
	mkdir -p ${DATADIRS}

down:
	@echo "Down-ing containers:"
	${COMPOSE} down

all: ${NAME}

######## INFO / DEBUGGING / TROUBLESHOOTING ########

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
	sudo sh -c "truncate -s 0 /var/lib/docker/containers/**/*-json.log"

restart:
	sudo service docker restart

talk:
	@PS3="Select for which container you want to access a shell: "; \
	select c in ${CONTAINERS}; \
	do echo "Shell for $$c:"; docker exec -it $$c ${SHELL}; exit $?; done

nginxlogs:
	@docker exec -it nginx cat /var/log/nginx/error.log

dbip:
	@docker exec -it mariadb hostname -i

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

define printname
	@if test 1 -eq "$$(tput cols | xargs printf '%s>100\n' | bc)"; then echo hello; fi
endef

.phony: fclean full all datadirs fix logs nginxlogs wlogs dbip info re talk clean down infor up
