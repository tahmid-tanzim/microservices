# Microservices

### Create a virtual environment to isolate our package dependencies locally
```shell
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### Install Django and Django REST framework into the virtual environment
```shell
pip install django
pip install djangorestframework
pip install django-cors-headers
pip install psycopg2-binary
pip install pika
```

### Django Migrations
```shell
docker-compose exec backend bash
python manage.py makemigrations
python manage.py migrate
```

### Flask Migrations
```shell
docker-compose exec backend bash
python manager.py db init
python manager.py db migrate
python manager.py db upgrade
```
