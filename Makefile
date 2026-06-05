.PHONY: dev build audit repair compose-up compose-down backup

dev:
	bash scripts/dev.sh

build:
	bash scripts/build.sh

audit:
	python3 scripts/audit_project.py

repair:
	python3 scripts/repair_project.py --json

compose-up:
	docker compose -f deploy/docker/docker-compose.yml up -d --build

compose-down:
	docker compose -f deploy/docker/docker-compose.yml down

backup:
	bash scripts/backup.sh
