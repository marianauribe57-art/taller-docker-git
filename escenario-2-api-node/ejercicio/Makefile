.PHONY: up down logs ps restart clean test

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

restart:
	docker compose restart

clean:
	docker compose down -v

db:
	docker compose exec db psql -U $${POSTGRES_USER} -d $${POSTGRES_DB}