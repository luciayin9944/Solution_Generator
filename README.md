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
