VOLUME=$(shell basename $(PWD))

develop: clean build migrations.upgrade run

clean:
	docker compose rm -vf

build:
	docker compose build

run:
	docker compose up

frontend-shell:
	docker compose run frontend \
	  sh

backend-shell:
	docker compose run worker \
	  sh

python-shell:
	docker compose run worker \
	  poetry run flask shell

# SQLite3 migrations (không cần PostgreSQL)
migrations.blank:
	docker compose run worker \
	  poetry run flask db revision

migrations.create:
	docker compose run worker \
	  poetry run flask db migrate

migrations.upgrade:
	docker compose run worker \
	  poetry run flask db upgrade

migrations.heads:
	docker compose run worker \
	  poetry run flask db heads

# Thêm target mới cho SQLite3
sqlite.init:
	docker compose run worker \
	  poetry run flask db init

sqlite.reset: clean
	docker compose run worker \
	  rm -f /srv/app.db || true
	docker compose run worker \
	  poetry run flask db upgrade
