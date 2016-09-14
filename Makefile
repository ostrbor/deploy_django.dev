SHELL = /bin/bash
.PHONY: dev prod clean

prod:
	cd Docker/ && docker-compose up -d

dev:
	cd Docker/ && docker-compose -f docker-compose-dev.yml up

clean:
	cd Docker/ && docker-compose down
ifneq ($(shell docker volume ls -f dangling=true -q),)
	docker volume rm $$(docker volume ls -f dangling=true -q)
endif
