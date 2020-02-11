# Docker compose file
export DOCKER_COMPOSE_FILE ?= docker-compose.yml
# Docker compose helpers
export DOCKER_COMPOSE = @docker-compose -f ${DOCKER_COMPOSE_FILE}
#
export DOCKER_IMAGE_NAME ?= alexkravsql
#
export DOCKER_FILE ?= Dockerfile

export MYSQL_USER=alex
export MYSQL_PASSWORD=kravchuk
export MYSQL_DATABASE=metrics
export MYSQL_ROOT_PASSWORD="qwerty"

all: help

.PHONY: help
# make help - Display callable targets
help:
	@printf "\nAvailable targets:\n\n"
	@egrep "^# make " [Mm]akefile
	@printf "\n"

.PHONY: docker/build
# make docker/build - Build docker image
docker/build:
	docker build -t ${DOCKER_IMAGE_NAME} . -f ${DOCKER_FILE} \
	--rm

.PHONY: docker-compose/config
# make docker-compose/config - Run docker-compose config
docker-compose/config:
	$(DOCKER_COMPOSE) config

.PHONY: docker-compose/ps
# make docker-compose/ps - Run docker-compose ps
docker-compose/ps:
	$(DOCKER_COMPOSE) ps

.PHONY: docker-compose/up
# make docker-compose/up - Builds, (re)creates, run in the background, and attaches to containers for a service.
docker-compose/up:
	$(DOCKER_COMPOSE) up -d

.PHONY: docker-compose/down
# make docker-compose/down - Stops containers and removes containers, networks, volumes, and images created by `up`.
docker-compose/down:
	$(DOCKER_COMPOSE) down

.PHONY: docker-compose/logs
# make docker-compose/logs - Get all containers logs
docker-compose/logs:
	$(DOCKER_COMPOSE) logs

.PHONY: docker-compose/restart
# make docker-compose/restart - Run docker-compose/down & docker-compose/up
docker-compose/restart: docker-compose/down docker-compose/up

.PHONY: docker-compose/rebuild
# make docker-compose/rebuild - Rebuild docker image and restart. Run docker/build docker-compose/up docker-compose/down
docker-compose/rebuild: docker/build docker-compose/restart
