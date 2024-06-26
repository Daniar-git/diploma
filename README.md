## Diplom project of Daniyar Usenkhanov, Abylaikhan Abdraman, Kanatyly Zhalgas

### Localhost:
- configure database in postgreSQL
- pip3 install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

### .env:
DEBUG=False
SECRET_KEY=django-insecure-w%^7^t)9-1i(0)h9ywxcvg3nvc8#mpt$v!2-q!+sw7doj!ku7l
DATABASE_NAME=diplom_user
DATABASE_USER=diplom_db
DATABASE_PASSWORD=1000
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432


## Init

##### Destroy docker containers and volumes
```bash
docker system prune -a
docker volume prune
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -a -q)
```

##### Docker (dev)
```bash
docker-compose run web python3 manage.py makemigrations
docker-compose run web python3 manage.py migrate
docker-compose run web python3 manage.py createsuperuser
docker-compose build --no-cache
docker-compose up
```