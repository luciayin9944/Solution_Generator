# MathApp-backend

## Requirements
### Install required package
```shell
pip install -r requirements.txt
```
### writerequirements.txt
```shell
pip freeze > requirements.txt
pipreqs --encoding utf-8
```

## Flask PostgreSQL
To connect database:

Host: math.csnsgshi11e2.us-east-2.rds.amazonaws.com

Port: 5432

Password: mathpassword


## Database

```shell
flask db init
```
```shell
flask db migrate -m "add note timestamp"
```
```shell
flask db upgrade
```
