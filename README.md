# Microservices


### Create a virtual environment to isolate our package dependencies locally
```bash
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### Install Django and Django REST framework into the virtual environment
```bash
pip install django
pip install djangorestframework
pip install django-cors-headers
pip install psycopg2-binary
pip install pika
```

`docker-compose exec backend bash`
