
default: help

.PHONY: shell
shell: ## Starts the Django interactive interpreter.
	python manage.py shell

.PHONY: migrations
migrations: ## Creates new migrations based on the changes detected to your models.
	python manage.py makemigrations

.PHONY: migrate
migrate: ## Synchronizes the database state with the current set of models and migrations.
	python manage.py migrate

.PHONY: createsuperuser
createsuperuser: ## Creates a default superuser.
	python manage.py createsuperuser --no-input; exit 0

.PHONY: runserver
runserver: ## Starts the Django development server.
	python manage.py runserver

.PHONY: help
help: ## Lists all the available commands.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
