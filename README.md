# hse-devops-hw04
![tests](https://github.com/TiunovNN/hse-devops-hw04/actions/workflows/python-app.yml/badge.svg)
## Автор
Тиунов Николай

## Описание

К нам обратился директор ветеринарной клиники и сказал:
"Клинике необходим микросервис для хранения и обновления информации для собак!"

Директор пообщался с IT-отделом, и они сверстали документацию в формате 
[OpenAPI](clinic.yaml).

## Запуск

```shell
$ docker-compose up -d
```

## Запуск тестов

```shell
$ pip install -r requirements.txt
$ pytest
```
