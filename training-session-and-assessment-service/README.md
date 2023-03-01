# FASTAPI with Micro Services
demo project for the learning purpose

## Table of contents

* [Objective of the project](#objective-of-the-project)
* [Prerequities](#prerequities)
* [Configure the project in local environment](#configure-the-project-in-local-environment)
* [Contributing Guidelines](#contributing-guidelines)
* [Command to start the application using docker](#command-to-start-the-application-using-docker)
* [Commands to start the application without docker](#commands-to-start-the-application-without-docker)


## Objective of the project
The demo project for the learning purpose based on FASTAPI and micro service structure

## Prerequities
* Python > 3.8.*
* postgresql

## Configure the project in local environment
* Clone the project from the reposetory [https://github.com/bhumilakum/fastapi-with-microservices-demo](https://github.com/bhumilakum/fastapi-with-microservices-demo)
* Create virtual environment
* Get pull in your local branch from the `main` branch for the latest code base.
* Checkout to the `main` branch for the latest code base
* Install requirements from `requirements.txt` file.
* Update the `.env` file with required local credentials details, one can take reference from the `.env.example` file.


## Contributing Guidelines
* Run command `pre-commit install`. Run this command from your git init root.
* Run command `pre-commit run -a`. This command will check python files and give result regarding formatting.
* After installing pre-commit hook, on each commit it will verify code standard formatting and will allow you to commit if all checks are passed.
* If you added these configs to an existing project, you may want to format whole code from the start. So for that, you just need to run command `pre-commit run --all-files`.

## Command to start the application using docker
```
 docker-compose up --build
````

## Commands to start the application without docker
```
uvicorn app.main:app --reload
```
