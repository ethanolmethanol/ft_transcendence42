NAME			= ft_transcendence

DATADIRS		= db/data/ front/dist/transcendence/browser/ ~/tr_certs

ENV_SRC			= ~/.env

ENV_FILE		= .env

# WIP
# DB_NAME		= $$(grep POSTGRES_DB ${ENV_FILE} | sed "s.POSTGRES_DB='(.*)'.\1.")

BROWSER			= firefox

SHELL			= bash

CONTAINERS		= back_auth back_user back_game front db prometheus grafana node_exporter blackbox_exporter redis

COMPOSE_PATH	= docker-compose.yml

COMPOSE			= docker compose -f ${COMPOSE_PATH}

R				= \033[1;31m # RED
G				= \033[1;32m # GREEN
Y				= \033[1;33m # YELLOW
C				= \033[1;34m # CYAN
M				= \033[1;35m # MAGENTA
N				= \033[0m    # RESET

TEST-ENGINE-TAGS = passed monitor paddle ball

# gen-cert 
${NAME}: up health
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

front/.stylelintrc.json:
	@echo -e "$(R)Woops! Looks like you don't have stylelint installed.$(N)"
	cd front && npm install stylelint && npm init stylelint

format-css: | front/.stylelintrc.json
	cd front && npx stylelint "**/*.css" --fix

%/venv:
	@echo -e "$(Y)Setting up new venv for $@.$(N)"
	@python3.12 -m venv $@

PY_SERVICES = back

PY_FMT_DEPS = $(addprefix /venv/bin/, black pylint flake8 isort mypy)

PY_MOD_DEPS = django pylint-django django-stubs djangorestframework-stubs djangorestframework django-health-check django-cors-headers psycopg2-binary werkzeug django-extensions pyOpenSSL

PYLINT_ARGS = --load-plugins pylint_django --django-settings-module transcendence_django.settings --disable=C0114 --disable=C0115 --disable=C0116 --disable=R0903 transcendence_django/back_*

$(addprefix %, $(PY_FMT_DEPS)): | %/venv
	@echo -e "$(Y)Installing dependencies for python linting (missing at least $(notdir $@)).$(N)"
	@cd $*/venv/bin && ./pip install $(notdir $(PY_FMT_DEPS)) $(PY_MOD_DEPS) > /dev/null

format-python: | $(foreach tool,$(PY_FMT_DEPS),$(addsuffix $(tool),$(PY_SERVICES)))
	for c in $(PY_SERVICES); do cd $$c; cp ../.github/linters/.flake8 .; $(foreach tool,$(PY_FMT_DEPS),echo -e "$(G)$(notdir $(tool)):$(N)"; .$(tool) $(if $(findstring pylint, $(tool)), $(PYLINT_ARGS), .); ) cd ..; done

format-cleanup:
	rm -rf $(addsuffix /venv, $(PY_SERVICES))
# pushd front && npm uninstall stylelint

lint: | $(foreach tool,$(PY_FMT_DEPS),$(addsuffix $(tool),$(PY_SERVICES)))
	docker run --rm \
		-e RUN_LOCAL=true \
		-e DEFAULT_BRANCH=$(shell git rev-parse --abbrev-ref HEAD) \
		--env-file ".github/super-linter.env" \
		-v "$(shell pwd)":/tmp/lint \
		ghcr.io/super-linter/super-linter:slim-latest

testform:
	python3 -m http.server -d back/test_form -b localhost 1234

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

test-engine:
	@PS3="Select a tag: "; \
	select TAG in ${TEST-ENGINE-TAGS}; do \
		if [ -n "$$TAG" ]; then \
			docker exec -it back_game pytest -m $$TAG; \
		fi; \
		break; \
	done


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

test:
	cd front/; npm run test

install-mkcert:
	@./scripts/install_mkcert.sh

gen-cert: install-mkcert
	@./scripts/gen_cert.sh

clean:
	@${COMPOSE} down -v

fclean: clean
	@docker --log-level=warn system prune -f
	@./scripts/gen_cert.sh clean

ffclean: fclean
	@docker --log-level=warn system prune -af
	@ rm -rf ${DATADIRS}
	@echo -e "$CDeleted data directories [$Y${DATADIRS}$C]$N"

re: fclean all

######## FUNKY STUFF ########

.PHONY: fclean full all datadirs fix logs nginxlogs wlogs dbip info re talk clean down infor up health install-mkcert gen-cert
.SILENT: health
