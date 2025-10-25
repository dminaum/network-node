.PHONY: install build up down restart logs test shell migrate makemigrations createsuperuser format lint clean check

# Poetry команды
install:
	poetry install

# Docker команды
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

# Django команды в Docker
shell:
	docker-compose exec web poetry run python manage.py shell

migrate:
	docker-compose exec web poetry run python manage.py migrate

makemigrations:
	docker-compose exec web poetry run python manage.py makemigrations

createsuperuser:
	docker-compose exec web poetry run python manage.py createsuperuser

check:
	docker-compose exec web poetry run python manage.py check

# Тестирование
test:
	docker-compose exec web poetry run pytest -vv

test-cov:
	docker-compose exec web poetry run pytest --cov=network_node --cov-report=html

test-local:
	poetry run pytest -vv

# Форматирование
format:
	poetry run black config network_node
	poetry run isort config network_node

lint:
	poetry run flake8 config network_node

# Локальная разработка
runserver:
	poetry run python manage.py runserver

# Очистка
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage

# Первый запуск
all: clean install build up migrate
