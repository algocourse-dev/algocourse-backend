# algocourse-backend (Development only)

### Setup virtual environment (Optional)
This is for checking package installation only

Create an "env" if needed:
```
python3 -m venv env
```

Activate virtual environment:
```
source env/bin/activate
```

Install required packages:
```
pip install -r app/requirements.txt
```

To deactivate virtual environment:
```
deactivate
```

### Install Docker
Install latest version of Docker via Docker's official website:
```
https://docs.docker.com/get-docker/
```

### Create images and run containers

Create a "db" directory (this is just a Docker volume, it can be empty, no worries)
```
mkdir db
```

Please make sure that these ports are free:
1. 1337 (nginx runs here)
2. 9090 (adminer runs here)
3. 6380 (redis runs here)

To modify port numbers, please refer to `docker-compose.yml`

cd to the root directory (parent of `app`)
```
docker-compose up -d --build
```
* -d, --detach: Detached mode: Run containers in the background, print new container names. Incompatible with --abort-on-container-exit.
* --build: Build images before starting containers.

To stop the containers and remove them
```
docker-compose down -v
```
* -v, --volumes: Remove named volumes declared in the `volumes` section of the Compose file and anonymous volumes attached to containers.

To see logs of containers
```
docker-compose logs -f
```
* -f, --follow: Follow log output.

To check files in the container
```
docker exec -it CONTAINER_ID /bin/sh
```

To list out the running containers
```
docker ps
```
* -a: list out all the containers, including the non-running ones

### After building up the containers, you can run these commands manually

Removes all data from the database and re-executes any post-synchronization handlers. The table of which migrations have been applied is not cleared. (More info: `https://docs.djangoproject.com/en/3.1/ref/django-admin/#flush`)
```
docker-compose exec web python manage.py flush --no-input
```

Synchronizes the database state with the current set of models and migrations (More info: `https://docs.djangoproject.com/en/3.1/ref/django-admin/#migrate`)
```
docker-compose exec web python manage.py migrate
```

Add static files (the static files are already here, may not need to run this command)
```
docker-compose exec web python manage.py collectstatic
```

### Feel free to develop from here `https://docs.djangoproject.com/en/3.1/`.

#### Update 26/12/2020:
Added pre-commit with pre-commit-hooks, isort, black and flake8.

When committing, there would be a number of jobs trying to lint the files. The commit will stop when there is at least one error while linting.

```isort``` is for sorting your imports (https://github.com/pycqa/isort).

```black``` is for formatting your code (https://github.com/psf/black).

```flake8``` is for linting your code (https://gitlab.com/pycqa/flake8).

You can run them independently with these commands:
```
isort .
black .
flake8 .
```

```isort``` and ```black``` will modify your files, you can use flag ```--diff``` to see how they change your files.

Configuration files:

```
isort: .isort.cfg
black: pyproject.toml
flake8: .flake8
pre-commit: pre-commit-config.yaml
```
